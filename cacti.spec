Summary:	Cacti is a php frontend for rrdtool
Summary(pl):	Cacti - frontend w PHP do rrdtoola
Name:		cacti
Version:	0.8.2a
Release:	1
License:	GPL
Group:		Applications/WWW
Source0:	http://www.raxnet.net/downloads/%{name}-%{version}.tar.gz
# Source0-md5:	d87613690e82e025412de6d747b0674e
#Patch0:		%{name}-%{version}-paths.patch.bz2
URL:		http://www.raxnet.net/
BuildRequires:	rpm-php-pearprov
Requires:	libnet-snmp50
Requires:	mysql
Requires:	net-snmp-utils
Requires:	net-snmp
Requires:	php
Requires:	php-gd
Requires:	php-mysql
Requires:	php-snmp
Requires:	rrdtool
Requires:	webserver
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

%description -l pl
Cacti to pe³ny frontent do rrdtoola, zapamiêtuj±cy wszystkie
informacje potrzebne do tworzenia wykresów i wype³niaj±ce je danymi w
bazie MySQL.

Frontend jest w pe³ni oparty na PHP. Oprócz zarz±dzania wykresami,
¼ród³ami danych, archiwami Round Robin w bazie danych, cacti obs³uguje
tak¿e gromadzenie danych. Ma tak¿e obs³ugê SNMP przydatn± przy
tworzeniu wykresów ruchu przy u¿yciu MRTG.

%prep
%setup -q
#%patch0 -p1

%build
# clean up CVS stuff
#for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
#	if [ -e "$i" ]; then rm -r $i; fi >/dev/null 2>&1
#done

# fix dir perms
#find . -type d | xargs chmod 755

# fix file perms
#find . -type f | xargs chmod 644

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{webadminroot}/%{name}

cp -aRf * $RPM_BUILD_ROOT%{webadminroot}/%{name}

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
