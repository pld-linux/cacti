%include	/usr/lib/rpm/macros.perl
Summary:	Cacti is a php frontend for rrdtool
Summary(pl):	Cacti - frontend w PHP do rrdtoola
Name:		cacti
Version:	0.8.4
Release:	2
License:	GPL
Group:		Applications/WWW
Source0:	http://www.raxnet.net/downloads/%{name}-%{version}.tar.gz
# Source0-md5:	afa100acd57db792dd65f4443268a64d
URL:		http://www.raxnet.net/
BuildRequires:	rpm-perlprov
Requires:	mysql
Requires:	net-snmp-utils
Requires:	net-snmp
Requires:	php
Requires:	php-gd
Requires:	php-mysql
Requires:	php-pcre
Requires:	php-snmp
Requires:	php-xml
Requires:	rrdtool
Requires:	webserver
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		webadminroot /srv/httpd

%description
Cacti is a complete frondend to rrdtool, it stores all of the
nessesary information to create graphs and populate them with data in
a MySQL database.

The frontend is completely PHP driven. Along with being able to
maintain Graphs, Data Sources, and Round Robin Archives in a database,
cacti handles the data gathering also. There is also SNMP support for
those used to creating traffic graphs with MRTG.

%description -l pl
Cacti to pe�ny frontent do rrdtoola, zapami�tuj�cy wszystkie
informacje potrzebne do tworzenia wykres�w i wype�niaj�ce je danymi w
bazie MySQL.

Frontend jest w pe�ni oparty na PHP. Opr�cz zarz�dzania wykresami,
�r�d�ami danych, archiwami Round Robin w bazie danych, cacti obs�uguje
tak�e gromadzenie danych. Ma tak�e obs�ug� SNMP przydatn� przy
tworzeniu wykres�w ruchu przy u�yciu MRTG.

%prep
%setup -q

%build

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
