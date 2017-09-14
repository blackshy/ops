from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, BooleanField, SubmitField, SelectField, HiddenField
from wtforms.validators import Required, Length, NumberRange, Email, Regexp, EqualTo, IPAddress
from wtforms import ValidationError
from flask_babel import lazy_gettext
from ..models import User
from .models import PhysicalServers, Vendors, VirtualServers, Platforms, OperateSystems, IPs, \
        NICRoles, NICs, DiskRoles, Disks, GPUs, Regions, Racks, ServerPositions, ServeStates, ServerTypes
from .. import db

class AddPhysicalServers(FlaskForm):
    #asset_tag = StringField(lazy_gettext('Asset tag'), validators=[Required(), Length(1, 128)])
    asset_tag = StringField('Asset tag', validators=[Required(), Length(1, 128)])
    hostname = StringField('Hostname', validators=[Length(1, 128)])
    opsers = StringField('Ops user', validators=[Required(), Length(1, 128)])
    developers = StringField('Dev user', validators=[Required(), Length(1, 128)])
    operate_system_id = SelectField('Choose OS', coerce=int, validators=[Required()])
    vendor_id = SelectField('Choose vendor', coerce=int, validators=[Required()])
    sn = StringField('SN', validators=[Required(), Length(1, 128)])
    mgmt_ip = StringField('Management IP', validators=[IPAddress(ipv4=True, ipv6=False, message=None)])
    description = TextAreaField('Description', validators=[Required()])
    submit = SubmitField('Add Server')

    def __init__(self, *args, **kwargs):
        super(AddPhysicalServers, self).__init__(*args, **kwargs)
        self.vendor_id.choices = [(v.id, v.company) for v in Vendors.query.order_by(Vendors.id).all()]
        self.operate_system_id.choices = [(v.id, v.os_distribution + ' - ' +
            str(v.os_release_major) + '.' + str(v.os_release_minor) + ' ' +
            v.os_release_code) for v in OperateSystems.query.order_by(OperateSystems.id).all()]

    def validate_asset_tag(self, field):
        if PhysicalServers.query.filter_by(asset_tag=field.data).first():
            raise ValidationError('Asset tag already used.')


class AddPlatforms(FlaskForm):
    name = StringField('Virtualization platform name', validators=[Required(), Length(1, 255)])
    description = TextAreaField('description', validators=[Required()])
    comment = TextAreaField('Comment')
    submit = SubmitField('Add Platform')


class AddOperateSystems(FlaskForm):
    os_distribution = StringField('OS distribution', validators=[Required(), Length(1, 128)])
    os_release_major = IntegerField('OS major number', validators=[Required(), NumberRange(1, 9999)])
    os_release_minor = IntegerField('OS minor number', validators=[NumberRange(1, 9999)])
    os_release_code = StringField('OS release code', validators=[Length(1, 128)])
    description = TextAreaField('Description', validators=[Required()])
    comment = TextAreaField('Comment')
    submit = SubmitField('Add OperateSystem')


class UpdateOperateSystems(FlaskForm):
    os_distribution = StringField('OS distribution', validators=[Required(), Length(1, 128)])
    os_release_major = IntegerField('OS major number', validators=[Required(), NumberRange(1, 9999)])
    os_release_minor = IntegerField('OS minor number', validators=[NumberRange(1, 9999)])
    os_release_code = StringField('OS release code', validators=[Length(1, 128)])
    description = TextAreaField('Description', validators=[Required()])
    comment = TextAreaField('Comment')
    submit = SubmitField('Add OperateSystem')

    def __init__(self, operate_system, *args, **kwargs):
        super(UpdateOperateSystems, self).__init__(*args, **kwargs)
        self.operate_system = operate_system


class AddIPs(FlaskForm):
    ip = StringField('IP', validators=[Required(), IPAddress(ipv4=True, ipv6=False, message=None)])
    netmask = StringField('Netmask', validators=[Required(), IPAddress(ipv4=True, ipv6=False, message=None)])
    gateway = StringField('Gateway', validators=[Required(), IPAddress(ipv4=True, ipv6=False, message=None)])
    in_use = BooleanField('Is in used ?')
    description = TextAreaField('Description', validators=[Required()])
    comment = TextAreaField('Comment')
    submit = SubmitField('Add IP')


class AddNetworks(FlaskForm):
    network = StringField('Network', validators=[Required(), IPAddress(ipv4=True, ipv6=False, message=None)])
    netmask = IntegerField('Netmask in CIDR', validators=[Required(), NumberRange(1,32)])
    gateway = StringField('Gateway', validators=[Required(), IPAddress(ipv4=True, ipv6=False, message=None)])
    in_use = BooleanField('Is in used ?')
    description = TextAreaField('Description', validators=[Required()])
    comment = TextAreaField('Comment')
    submit = SubmitField('Add Network')

    def __init__(self, *args, **kwargs):
        super(AddNetworks, self).__init__(*args, **kwargs)
        self.position_id.choices = [(v.id, v.company) for v in Vendors.query.order_by(Vendors.id).all()]
        self.os_id.choices = [(v.id, v.os_distribution + ' - ' +
            str(v.os_release_major) + '.' + str(v.os_release_minor) + ' ' +
            v.os_release_code) for v in OperateSystems.query.order_by(OperateSystems.id).all()]

    def validate_asset_tag(self, field):
        if PhysicalServers.query.filter_by(asset_tag=field.data).first():
            raise ValidationError('Asset tag already used.')



class AddVendors(FlaskForm):
    company = StringField('company', validators=[Required(), Length(1, 255)])
    email = StringField('email', validators=[Required(), Email(), Length(1, 255)])
    mobile = StringField('mobile', validators=[Length(1, 255)])
    phone = StringField('phone', validators=[Length(1, 255)])
    user = StringField('user', validators=[Required(), Length(1, 255)])
    description = TextAreaField('description', validators=[Required()])
    comment = TextAreaField('comment')
    submit = SubmitField('Add Vendors')


class AddRegions(FlaskForm):
    trusteeship = StringField('trusteeship', validators=[Required(), Length(1, 255)])
    region = StringField('region', validators=[Required(), Length(1, 255)])
    sub_region = StringField('sub_region', validators=[Length(0, 255)])
    description = TextAreaField('description', validators=[Required()])
    comment = TextAreaField('comment')
    submit = SubmitField('Add Region')


class AddRacks(FlaskForm):
    region = SelectField('Region', coerce=int)
    rack = StringField('Rack', validators=[Required(), Length(1,255)])
    description = TextAreaField('Description', validators=[Required()])
    comment = TextAreaField('Comment')
    submit = SubmitField('Add Rack')

    def __init__(self, *args, **kwargs):
        super(AddRacks, self).__init__(*args, **kwargs)
        self.region.choices = [(v.id, v.trusteeship + ' - ' +
            v.region + '-' + v.sub_region) for v in Regions.query.order_by(Regions.trusteeship).all()]


class AddServerPositions(FlaskForm):
    rack = SelectField('Rack', coerce=int)
    number = IntegerField('Number', validators=[Required(), NumberRange(1,999)])
    description = TextAreaField('Description', validators=[Required()])
    comment = TextAreaField('Comment')
    submit = SubmitField('Add Server Position')


class AddNICRoles(FlaskForm):
    name = StringField('Name', validators=[Required(), Length(1,255)])
    description = TextAreaField('Description', validators=[Required()])
    comment = TextAreaField('Comment')
    submit = SubmitField('Add NIC Role')

class AddNICs(FlaskForm):
    sn = StringField('SN', validators=[Length(0, 255)])
    speed = IntegerField('Speed', validators=[Required(), NumberRange(1, 999999)])
    mac_address = StringField('MAC Address', validators=[Length(0, 255)])
    nic_role_id = SelectField('NIC Type', coerce=int, validators=[Required()])
    vendor_id = SelectField('Choose Vendor', coerce=int, validators=[Required()]) 
    in_use = BooleanField('Is in used ?')
    description = TextAreaField('Description', validators=[Required()])
    comment = TextAreaField('comment')
    submit = SubmitField('Add NIC')

class AddDiskRoles(FlaskForm):
    storage_type = StringField('Storage Type', validators=[Required(), Length(1, 64)])
    plug_type = StringField('Plugin Type', validators=[Required(), Length(1, 64)])
    speed = IntegerField('RPM Speed', validators=[Required(), NumberRange(1, 999999)])
    description = TextAreaField('Description', validators=[Required()])
    comment = TextAreaField('Comment')
    submit = SubmitField('Add Disk Role')


class AddDisks(FlaskForm):
    sn = StringField('SN', validators=[Length(0, 255)])
    size = IntegerField('Size', validators=[NumberRange(1, 999999)])
    in_use = BooleanField('Is in used ?')
    #physical_server_id = SelectField('Choose Physical Server', coerce=int)
    vendor_id = SelectField('Choose Vendor', coerce=int, validators=[Required()])
    disk_role_id = SelectField('Choose Disk Role', coerce=int, validators=[Required()])
    description = TextAreaField('Description', validators=[Required()])
    comment = TextAreaField('Comment')
    submit = SubmitField('Add Disk')
