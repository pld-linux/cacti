%define name	cacti
%define version	0.6.8a
%define release	3mdk
%define webadminroot /var/www/html/admin

Summary:	Cacti is a php frontend for rrdtool
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Servers
URL:		http://www.raxnet.net/
Source0:	%{name}-%{version}.tar.bz2
Patch0:		%{name}-%{version}-paths.patch.bz2
Requires:	webserver mysqlserver mod_php php php-common php-gd php-mysql php-snmp
Requires:	net-snmp-utils libnet-snmp50 net-snmp net-snmp-mibs
Requires:	librrdtool0 rrdtool
BuildRequires:	perl
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
BuildArch:	noarch
Prefix:		%{webadminroot}

%description
Cacti is a complete frondend to rrdtool, it stores all of the
nessesary information to create graphs and populate them with
data in a MySQL database.

The frontend is completely PHP driven. Along with being able
to maintain Graphs, Data Sources, and Round Robin Archives in
a database, cacti handles the data gathering also. There is
also SNMP support for those used to creating traffic graphs
with MRTG.

%prep

%setup -q
%patch0 -p1

%build

# clean up CVS stuff
for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -r $i; fi >&/dev/null
done

# fix dir perms
find . -type d | xargs chmod 755

# fix file perms
find . -type f | xargs chmod 644

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

mkdir -p %{buildroot}%{webadminroot}/%{name}
cp -aRf * %{buildroot}%{webadminroot}/%{name}/

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot} 

%files
%defattr(-, root, root)
%doc docs/CHANGELOG docs/CONTRIB docs/README
%config(noreplace) %attr(0644,apache,apache) %{webadminroot}/%{name}/log/rrd.log
%config(noreplace) %attr(0644,root,root) %{webadminroot}/%{name}/rra/.placeholder
%config(noreplace) %attr(0644,apache,apache) %{webadminroot}/%{name}/include/config.php
%{webadminroot}/%{name}/*

%changelog
* Thu Jan 16 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.6.8a-3mdk
- build release

* Thu Sep 19 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.6.8a-2mdk
- misc spec file fixes
- install in common and relocatable %%{webadminroot}/ directory

* Wed Sep 18 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.6.8a-1mdk
- security release
- do not require non existant php extensions
- misc spec file fixes 

* Sun May 12 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.6.8-1mdk
- initial cooker contrib
