from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
            current_user
from . import assets
from .. import db
from .models import PhysicalServers, VirtualServers, GPUs, Disks, \
        Vendors, NICs, OperateSystems, IPs, Regions, Racks, ServerPositions, \
        NICRoles, NICs, DiskRoles, Disks
from .forms import AddPhysicalServers, AddVendors, AddOperateSystems, \
        AddRegions, AddRacks, AddServerPositions, AddNICRoles, AddNICs, \
        AddDiskRoles, AddDisks, AddIPs, UpdateOperateSystems
import requests
import json


@assets.route('/physicalservers', methods=['GET'])
def physical_servers():
    physical_servers = PhysicalServers.query.all()
    return render_template('assets/physical_servers.html', \
            physical_servers=physical_servers)


@assets.route('/physicalservers/add', methods=['GET', 'POST'])
def physical_servers_add():
    form = AddPhysicalServers()
    if form.validate_on_submit():
        physical_server = PhysicalServers(
                asset_tag=form.asset_tag.data,
                hostname=form.hostname.data,
                opsers=form.opsers.data,
                vendor_id=form.vendor_id.data,
                operate_system_id=form.operate_system_id.data,
                developers=form.developers.data,
                sn=form.sn.data,
                description=form.description.data
                )
        db.session.add(physical_server)
        db.session.commit()
        return redirect(url_for('assets.physical_servers'))
    return render_template('assets/physical_servers_add.html', form=form)


@assets.route('/physicalservers/update', methods=['GET', 'POST'])
def physical_servers_update():
    pass


@assets.route('/physicalservers/delete', methods=['GET', 'POST'])
def physical_servers_delete():
    pass


@assets.route('/virtualservers', methods=['GET', 'POST'])
def virtual_servers():
    return render_template('assets/virtual_servers.html')


@assets.route('/virtualservers/add', methods=['GET', 'POST'])
def virtual_servers_add():
    pass


@assets.route('/virtualservers/update', methods=['GET', 'POST'])
def virtual_servers_update():
    pass


@assets.route('/virtualservers/delete', methods=['GET', 'POST'])
def virtual_servers_delete():
    pass


@assets.route('/vendors', methods=['GET'])
def vendors():
    vendors = Vendors.query.all()
    return render_template('assets/vendors.html', vendors=vendors)


@assets.route('/vendors/add', methods=['GET', 'POST'])
def vendors_add():
    form = AddVendors()
    if form.validate_on_submit():
        vendors = Vendors(
                company=form.company.data,
                email=form.email.data,
                mobile=form.mobile.data,
                phone=form.phone.data,
                description=form.description.data,
                comment=form.comment.data)
        db.session.add(vendors)
        db.session.commit()
        return redirect(url_for('assets.vendors'))
    return render_template('assets/vendors_add.html', form=form)


@assets.route('/vendors/update', methods=['GET', 'POST'])
def vendor_update():
    pass


@assets.route('/vendors/delete', methods=['GET', 'POST'])
def vendor_delete():
    pass


@assets.route('/platforms', methods=['GET'])
def platforms():
    pass


@assets.route('/platforms/add', methods=['GET', 'POST'])
def platforms_add():
    pass


@assets.route('/platforms/update', methods=['GET', 'POST'])
def platforms_update():
    pass


@assets.route('/platforms/delete', methods=['GET', 'POST'])
def platforms_delete():
    pass


@assets.route('/operatesystems', methods=['GET', 'POST'])
def operate_systems():
    operate_systems = OperateSystems.query.all()
    return render_template('assets/operate_systems.html', \
            operate_systems=operate_systems)


@assets.route('/operatesystems/add', methods=['GET', 'POST'])
def operate_systems_add():
    form = AddOperateSystems()
    if form.validate_on_submit():
        operate_system = OperateSystems(
                os_distribution=form.os_distribution.data,
                os_release_major=form.os_release_major.data,
                os_release_minor=form.os_release_minor.data,
                os_release_code=form.os_release_code.data,
                description=form.description.data,
                comment=form.comment.data
                )
        db.session.add(operate_system)
        db.session.commit()
        return redirect(url_for('assets.operate_systems'))
    return render_template('assets/operate_systems_add.html', form=form)


@assets.route('/operatesystems/update/<int:post_id>', methods=['GET', 'POST'])
def operate_systems_update(post_id):
    operate_system = OperateSystems.query.get_or_404(post_id)
    form = UpdateOperateSystems(operate_system=operate_system)
    if form.validate_on_submit():
        operate_system.os_distribution=form.os_distribution.data
        operate_system.os_release_major=form.os_release_major.data
        operate_system.os_release_minor=form.os_release_minor.data
        operate_system.os_release_code=form.os_release_code.data
        operate_system.description=form.description.data
        operate_system.comment=form.comment.data
        db.session.add(operate_system)
        flash('The Operate System has been update!')
        return redirect(url_for('assets.operate_systems'))
    form.os_distribution.data = operate_system.os_distribution
    form.os_release_major.data = operate_system.os_release_major
    form.os_release_minor.data = operate_system.os_release_minor
    form.os_release_code.data = operate_system.os_release_code
    form.description.data = operate_system.description
    form.comment.data = operate_system.comment
    return render_template('assets/operate_systems_add.html', form=form)


@assets.route('/operatesystems/delete/<int:post_id>', methods=['GET', 'POST'])
def operate_systems_delete(post_id):
    operate_system = OperateSystems.query.get_or_404(post_id)
    os = OperateSystems()
    os.delete(operate_system)
    return redirect(url_for('assets.operate_systems'))



@assets.route('/ips', methods=['GET', 'POST'])
def ips():
    ips = IPs.query.order_by(IPs.ip).all()
    return render_template('assets/ips.html', \
            ips=ips)


@assets.route('/ips/add', methods=['GET', 'POST'])
def ips_add():
    form = AddIPs()
    if form.validate_on_submit():
        ips = IPs(
                ip=form.ip.data,
                netmask=form.netmask.data,
                cidr=form.cidr.data,
                gateway=form.gateway.data,
                in_use=form.in_use.data,
                description=form.description.data,
                comment=form.comment.data
                )
        db.session.add(ips)
        db.session.commit()
        return redirect(url_for('assets.ips'))
    return render_template('assets/ips_add.html', form=form)


@assets.route('/ips/update', methods=['GET', 'POST'])
def ips_update():
    pass


@assets.route('/ips/delete', methods=['GET', 'POST'])
def ips_delete():
    pass


@assets.route('/regions', methods=['GET'])
def regions():
    regions = Regions.query.order_by(Regions.trusteeship).all()
    return render_template('assets/regions.html', \
            regions=regions)


@assets.route('/regions/add', methods=['GET', 'POST'])
def regions_add():
    form = AddRegions()
    if form.validate_on_submit():
        regions = Regions(
                trusteeship=form.trusteeship.data,
                region=form.region.data,
                sub_region=form.sub_region.data,
                description=form.description.data,
                comment=form.comment.data
                )
        db.session.add(regions)
        db.session.commit()
        return redirect(url_for('assets.regions'))
    return render_template('assets/regions_add.html', form=form)


@assets.route('/racks', methods=['GET'])
def racks():
    racks = Racks.query.filter(Racks.regions.any()).all()
    return render_template('assets/racks.html', \
            racks=racks)

@assets.route('/racks/add', methods=['GET', 'POST'])
def racks_add():
    form = AddRacks()
    if form.validate_on_submit():
        racks = Racks(
                rack=form.rack.data,
                description=form.description.data,
                comment=form.comment.data
                )
        racks.regions.append(Regions.query.get(form.region.data))
        db.session.add(racks)
        db.session.commit()
        return redirect(url_for('assets.racks'))
    return render_template('assets/racks_add.html', form=form)


@assets.route('/nics', methods=['GET'])
def nics():
    nics = NICs.query.all()
    return render_template('assets/nics.html', \
            nics=nics)


@assets.route('/nics/add', methods=['GET', 'POST'])
def nics_add():
    form = AddNICs()
    form.vendor_id.choices = [(v.id, v.company) for v in Vendors.query.all()]
    form.nic_role_id.choices = [(v.id, v.name) for v in NICRoles.query.all()]
    if form.validate_on_submit():
        nics = NICs(
                sn=form.sn.data,
                speed=form.speed.data,
                mac_address=form.mac_address.data,
                vendor_id=form.vendor_id.data,
                nic_role_id=form.nic_role_id.data,
                in_use=form.in_use.data,
                description=form.description.data,
                comment=form.comment.data
                )
        db.session.add(nics)
        db.session.commit()
        return redirect(url_for('assets.nics'))
    return render_template('assets/nics_add.html', form=form)


@assets.route('/nicroles', methods=['GET'])
def nicroles():
    nicroles = NICRoles.query.all()
    return render_template('assets/nicroles.html', \
            nicroles=nicroles)


@assets.route('/nicroles/add', methods=['GET', 'POST'])
def nicroles_add():
    form = AddNICRoles()
    if form.validate_on_submit():
        nicroles = NICRoles(
                name=form.name.data,
                description=form.description.data,
                comment=form.comment.data
                )
        db.session.add(nicroles)
        db.session.commit()
        return redirect(url_for('assets.nicroles'))
    return render_template('assets/nicroles_add.html', form=form)


@assets.route('/disk_roles', methods=['GET'])
def disk_roles():
    disk_roles = DiskRoles.query.all()
    return render_template('assets/disk_roles.html', \
            disk_roles=disk_roles)


@assets.route('/disk_roles/add', methods=['GET', 'POST'])
def disk_roles_add():
    form = AddDiskRoles()
    if form.validate_on_submit():
        disk_roles = DiskRoles(
                storage_type=form.storage_type.data,
                plug_type=form.plug_type.data,
                speed=form.speed.data,
                description=form.description.data,
                comment=form.comment.data
                )
        db.session.add(disk_roles)
        db.session.commit()
        return redirect(url_for('assets.disk_roles'))
    return render_template('assets/disk_roles_add.html', form=form)


@assets.route('/disks', methods=['GET'])
def disks():
    disks = Disks.query.all()
    return render_template('assets/disks.html', \
            disks=disks)


@assets.route('/disks/add', methods=['GET', 'POST'])
def disks_add():
    form = AddDisks()
    form.vendor_id.choices = [(v.id, v.company) for v in Vendors.query.all()]
    form.disk_role_id.choices = [(v.id, v.storage_type + ' ' +
        v.plug_type + ' ' + str(v.speed) + ' rpm') for v in DiskRoles.query.all()]
    if form.validate_on_submit():
        disks = Disks(
                sn=form.sn.data,
                size=form.size.data,
                in_use=form.in_use.data,
                vendor_id=form.vendor_id.data,
                disk_role_id=form.disk_role_id.data,
                description=form.description.data,
                comment=form.comment.data
                )
        db.session.add(disks)
        db.session.commit()
        return redirect(url_for('assets.disks'))
    return render_template('assets/disks_add.html', form=form)
