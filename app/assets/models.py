from .. import db
from datetime import datetime, timedelta


class PhysicalServers(db.Model):
    __tablename__ = 'physical_servers'
    id = db.Column(db.Integer, primary_key=True)
    asset_tag = db.Column(db.String(255), unique=True)
    hostname = db.Column(db.String(255))
    primary_ip = db.Column(db.String(64))
    second_ip = db.Column(db.String(64))
    other_ip = db.Column(db.String(64))
    route_info = db.Column(db.Text)
    mgmt_ip = db.Column(db.String(64))
    opsers = db.Column(db.String(255))
    developers = db.Column(db.String(255))
    sn = db.Column(db.String(255))
    gpu_info = db.Column(db.Text)
    ib_info = db.Column(db.Text)
    dns_info = db.Column(db.Text)
    disk_info = db.Column(db.Text)
    nic_info = db.Column(db.Text)
    raid_info = db.Column(db.Text)
    kernel_info = db.Column(db.Text)
    cpu_info = db.Column(db.Text)
    memory_info = db.Column(db.Text)
    packages = db.Column(db.Text)
    partitions = db.Column(db.Text)
    sysctls = db.Column(db.Text)
    lvms = db.Column(db.Text)
    description = db.Column(db.Text)
    comment = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime, default=datetime.now())

    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'))
    operate_system_id = db.Column(db.Integer, db.ForeignKey('operate_systems.id'))
    serve_state_id = db.Column(db.Integer, db.ForeignKey('serve_states.id'))
    server_type_id = db.Column(db.Integer, db.ForeignKey('server_types.id'))

    vendor = db.relationship('Vendors', backref='physical_server_vendor')
    serve_state = db.relationship('ServeStates', backref='physical_server_serve_state')
    server_type = db.relationship('ServerTypes', backref='physical_server_server_type')


class VirtualServers(db.Model):
    __tablename__ = 'virtual_servers'
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(255))
    opsers = db.Column(db.String(255))
    developers = db.Column(db.String(255))
    description = db.Column(db.Text)
    online_tag = db.Column(db.Boolean)
    uuid = db.Column(db.String(128))
    cpu_total_count = db.Column(db.Integer)
    cpu_sockets_count = db.Column(db.Integer)
    cpu_cores_per_socket = db.Column(db.Integer)
    cpu_threads_per_core = db.Column(db.Integer)
    cpu_vender = db.Column(db.String(255))
    cpu_model_name = db.Column(db.String(255))
    memory_size_gb = db.Column(db.Integer)
    swap_size_gb = db.Column(db.Integer)
    nics = db.relationship('NICs', backref='virtual_server_nic')
    platform_id = db.Column(db.Integer, db.ForeignKey('platforms.id'))
    os_id = db.Column(db.Integer, db.ForeignKey('operate_systems.id'))
    kernel_version = db.Column(db.String(64))
    kernel_args = db.Column(db.String(255))
    kernel_arch = db.Column(db.String(64))
    bios_type = db.Column(db.String(64))
    packages = db.Column(db.Text)
    disks_dev = db.Column(db.String(500))
    partition = db.Column(db.String(500))
    mount_point = db.Column(db.String(500))
    sysctls = db.Column(db.String(500))
    lvs = db.Column(db.String(500))
    vgs = db.Column(db.String(500))
    pvs = db.Column(db.String(500))
    server_type = db.Column(db.Integer)
    mgmt_ip = db.Column(db.String(255))
    comment = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime, default=datetime.now())


class Platforms(db.Model):
    __tablename__ = 'platforms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.Text)
    comment = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime, default=datetime.now())


class OperateSystems(db.Model):
    __tablename__ = 'operate_systems'
    id = db.Column(db.Integer, primary_key=True)
    os_distribution = db.Column(db.String(64))
    os_release_major = db.Column(db.SmallInteger)
    os_release_minor = db.Column(db.SmallInteger)
    os_release_code = db.Column(db.String(64))
    description = db.Column(db.Text)
    comment = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime, default=datetime.now())

    operate_system = db.relationship('PhysicalServers', backref='operate_system_physical_server')

    def delete(self, operate_system):
        db.session.delete(operate_system)

class IPs(db.Model):
    __tablename__ = 'ips'
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(64), unique=True)
    netmask = db.Column(db.String(64))
    gateway = db.Column(db.String(64))
    in_use = db.Column(db.Boolean)
    description = db.Column(db.Text)
    comment = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime, default=datetime.now())

    def delete(self, ip):
        db.session.delete(ip)


class Networks(db.Model):
    __tablename__ = 'networks'
    id = db.Column(db.Integer, primary_key=True)
    network = db.Column(db.String(64), unique=True)
    netmask = db.Column(db.Integer)
    gateway = db.Column(db.Boolean)
    description = db.Column(db.Text)
    comment = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime, default=datetime.now())

    region_id = db.Column(db.Integer, db.ForeignKey('regions.id'))
    region = db.relationship('Regions', backref='network_region')

    def delete(self, network):
        db.session.delete(network)


class NICRoles(db.Model):
    __tablename__ = 'nic_roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    nics = db.relationship('NICs', backref='role_nic')
    description = db.Column(db.Text)
    comment = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime, default=datetime.now())

class NICs(db.Model):
    __tablename__ = 'nics'
    id = db.Column(db.Integer, primary_key=True)
    sn = db.Column(db.String(255), unique=True)
    speed = db.Column(db.String(64))
    mac_address = db.Column(db.String(255))
    nic_role_id = db.Column(db.Integer, db.ForeignKey('nic_roles.id'))
    physical_server_id = db.Column(db.Integer, db.ForeignKey('physical_servers.id'))
    virtual_server_id = db.Column(db.Integer, db.ForeignKey('virtual_servers.id'))
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'))
    in_use = db.Column(db.Boolean)
    description = db.Column(db.Text)
    comment = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime, default=datetime.now())

    vendor = db.relationship('Vendors', backref='nic_vendor')
    nicrole = db.relationship('NICRoles', backref='nicrole')


class DiskRoles(db.Model):
    __tablename__ = 'disk_roles'
    id = db.Column(db.Integer, primary_key=True)
    storage_type = db.Column(db.String(64))
    plug_type = db.Column(db.String(64))
    speed = db.Column(db.Integer)
    description = db.Column(db.Text)
    comment = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime, default=datetime.now())

class Disks(db.Model):
    __tablename__ = 'disks'
    id = db.Column(db.Integer, primary_key=True)
    sn = db.Column(db.String(255), unique=True)
    size = db.Column(db.String(64))
    in_use = db.Column(db.Boolean)
    physical_server_id = db.Column(db.Integer, db.ForeignKey('physical_servers.id'))
    disk_role_id = db.Column(db.Integer, db.ForeignKey('disk_roles.id'))
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'))
    description = db.Column(db.Text)
    comment = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime, default=datetime.now())

    vendor = db.relationship('Vendors', backref='disk_vendor')
    disk_role = db.relationship('DiskRoles', backref='disk_role')

class GPUs(db.Model):
    __tablename__ = 'gpus'
    id = db.Column(db.Integer, primary_key=True)
    sn = db.Column(db.String(255), unique=True)
    type = db.Column(db.String(255))
    cores_per_card = db.Column(db.Integer)
    in_use = db.Column(db.Boolean)
    physical_server_id = db.Column(db.Integer, db.ForeignKey('physical_servers.id'))
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'))
    description = db.Column(db.Text)
    comment = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime, default=datetime.now())

class Vendors(db.Model):
    __tablename__ = 'vendors'
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255))
    mobile = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    user = db.Column(db.String(255))
    description = db.Column(db.Text)
    comment = db.Column(db.Text)
    nics = db.relationship('NICs', backref='vendor_nic')
    disks = db.relationship('Disks', backref='vendor_disk')
    gpus = db.relationship('GPUs', backref='vendor_gpu')
    physical_servers = db.relationship('PhysicalServers', backref='vendor_physical_server')
    create_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime, default=datetime.now())


positions = db.Table('positions', 
        db.Column('region_id', db.Integer, db.ForeignKey('regions.id')),
        db.Column('rack_id', db.Integer, db.ForeignKey('racks.id'))
        )

in_rack_positions = db.Table('in_rack_positions',
        db.Column('rack_id', db.Integer, db.ForeignKey('racks.id')),
        db.Column('server_position_id', db.Integer, db.ForeignKey('server_positions.id'))
        )


class Regions(db.Model):
    __tablename__ = 'regions'
    id = db.Column(db.Integer, primary_key=True)
    trusteeship = db.Column(db.String(255))
    region = db.Column(db.String(255))
    sub_region = db.Column(db.String(255))
    description = db.Column(db.Text)
    comment = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime, default=datetime.now())

    def delete(self, region):
        db.session.delete(region)


class Racks(db.Model):
    __tablename__ = 'racks'
    id = db.Column(db.Integer, primary_key=True)
    rack = db.Column(db.String(255))
    description = db.Column(db.Text)
    comment = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime, default=datetime.now())

    regions = db.relationship('Regions', secondary=positions,
            backref=db.backref('racks', lazy='dynamic'),
            lazy='dynamic')

    def delete(self, rack):
        db.session.delete(rack)


class ServerPositions(db.Model):
    __tablename__ = 'server_positions'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    description = db.Column(db.Text)
    comment = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime, default=datetime.now())

    racks = db.relationship('Racks', secondary=in_rack_positions,
            backref=db.backref('server_positons', lazy='dynamic'),
            lazy='dynamic')

    def delete(self, server_position):
        db.session.delete(server_position)

class ServeStates(db.Model):
    __tablename__ = 'serve_states'
    id = db.Column(db.Integer, primary_key=True)
    state  = db.Column(db.String(255), unique=True)
    description = db.Column(db.Text)
    comment = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime, default=datetime.now())


class ServerTypes(db.Model):
    __tablename__ = 'server_types'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(255), unique=True)
    description = db.Column(db.Text)
    comment = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime, default=datetime.now())
