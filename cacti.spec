# TODO:
# - move config files to /etc/%{name}
# - add apache config
# - security http://security.gentoo.org/glsa/glsa-200506-20.xml
%include	/usr/lib/rpm/macros.perl
Summary:	Cacti is a PHP frontend for rrdtool
Summary(pl):	Cacti - frontend w PHP do rrdtoola
Name:		cacti
Version:	0.8.6c
Release:	0.1
License:	GPL
Group:		Applications/WWW
Source0:	http://www.cacti.net/downloads/%{name}-%{version}.tar.gz
# Source0-md5:	f48b1cc12ebdf96358563760c812e227
URL:		http://www.cacti.net/
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

%define		webadminroot /usr/share/%{name}

%description
Cacti is a complete frondend to rrdtool, it stores all of the
nessesary information to create graphs and populate them with data in
a MySQL database.

The frontend is completely PHP driven. Along with being able to
maintain Graphs, Data Sources, and Round Robin Archives in a database,
cacti handles the data gathering also. There is also SNMP support for
those used to creating traffic graphs with MRTG.

%description -l pl
Cacti to pe³ny frontend do rrdtoola, zapamiêtuj±cy wszystkie
informacje potrzebne do tworzenia wykresów i wype³niaj±ce je danymi w
bazie MySQL.

Frontend jest w pe³ni oparty na PHP. Oprócz zarz±dzania wykresami,
¼ród³ami danych, archiwami Round Robin w bazie danych, cacti obs³uguje
tak¿e gromadzenie danych. Ma tak¿e obs³ugê SNMP przydatn± przy
tworzeniu wykresów ruchu przy u¿yciu MRTG.

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
%dir %{webadminroot}
%dir %{webadminroot}/%{name}
%dir %{webadminroot}/%{name}/log
%config(noreplace) %verify(not size mtime md5) %attr(644,http,http) %{webadminroot}/%{name}/log/cacti.log
%dir %{webadminroot}/%{name}/rra
%config(noreplace) %verify(not size mtime md5) %{webadminroot}/%{name}/rra/.placeholder
%dir %{webadminroot}/%{name}/include
%config(noreplace) %verify(not size mtime md5) %attr(644,http,http) %{webadminroot}/%{name}/include/config.php
%{webadminroot}/%{name}/*
