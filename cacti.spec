Summary:	Cacti is a php frontend for rrdtool
Name:		cacti
Version:	0.6.8a
Release:	4
License:	GPL
Group:		Applications/WWW
Source0:	http://www.raxnet.net/downloads/%{name}-%{version}.tar.gz
# Source0-md5:	8466cf3dbd3125778a2f4f2be2f73e38
#Patch0:		%{name}-%{version}-paths.patch.bz2
URL:		http://www.raxnet.net/
BuildRequires:	perl
Requires:	webserver
Requires:	libnet-snmp50
Requires:	mysql
Requires:	net-snmp-utils
Requires:	net-snmp
Requires:	php
Requires:	php-gd
Requires:	php-mysql
Requires:	php-snmp
Requires:	rrdtool
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		webadminroot /home/services/httpd

%description
Cacti is a complete frondend to rrdtool, it stores all of the
nessesary information to create graphs and populate them with data in
a MySQL database.

The frontend is completely PHP driven. Along with being able to
maintain Graphs, Data Sources, and Round Robin Archives in a database,
cacti handles the data gathering also. There is also SNMP support for
those used to creating traffic graphs with MRTG.

%prep
%setup -q
#%patch0 -p1

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
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{webadminroot}/%{name}
cp -aRf * $RPM_BUILD_ROOT%{webadminroot}/%{name}/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc docs/CHANGELOG docs/CONTRIB docs/README
%dir %{webadminroot}/%{name}
%config(noreplace) %verify(not size mtime md5) %attr(644,http,http) %{webadminroot}/%{name}/log/rrd.log
%config(noreplace) %verify(not size mtime md5) %{webadminroot}/%{name}/rra/.placeholder
%config(noreplace) %verify(not size mtime md5) %attr(644,http,http) %{webadminroot}/%{name}/include/config.php
%{webadminroot}/%{name}/*
