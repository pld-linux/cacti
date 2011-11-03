#
# Conditional build:
%bcond_without	pa		# without plugin archidecture patch

%define		pia_ver	3.0
%include	/usr/lib/rpm/macros.perl
Summary:	Cacti is a PHP frontend for rrdtool
Summary(pl.UTF-8):	Cacti - frontend w PHP do rrdtoola
Name:		cacti
Version:	0.8.7h
Release:	2
License:	GPL
Group:		Applications/WWW
Source0:	http://www.cacti.net/downloads/%{name}-%{version}.tar.gz
# Source0-md5:	58c9371341f49a190ae11a85118e598d
Source2:	%{name}.crontab
Source3:	%{name}-apache.conf
Source4:	%{name}-lighttpd.conf
Source5:	%{name}-rrdpath.sql
Source6:	%{name}-pa.sql
Source7:	%{name}.logrotate
# http://docs.cacti.net/manual:087:1_installation.9_pia
Source8:	http://www.cacti.net/downloads/pia/%{name}-plugin-%{version}-PA-v%{pia_ver}.tar.gz
# Source8-md5:	1f45a65dc76dee368b11f2c78ae89dfb
# NOTE: update provides: cacti(pia) when updating the patch
Patch0:		%{name}-PA.patch
Patch1:		%{name}-config.patch
Patch2:		%{name}-adodb.patch
Patch3:		%{name}-ioerror.patch
Patch4:		%{name}-webroot.patch
Patch5:		%{name}-linux_memory.patch
Patch6:		%{name}-log-verbosity.patch
Patch7:		%{name}-ss_disk-array-indices.patch
Patch8:		host_name-url.patch
# http://www.cacti.net/download_patches.php
#Patch10:	none now
URL:		http://www.cacti.net/
BuildRequires:	rpm-perlprov
BuildRequires:	sed >= 4.0
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/useradd
Requires:	adodb >= 4.67-1.17
Requires:	crondaemon
Requires:	group(http)
Requires:	net-snmp-utils
Requires:	php-cli
Requires:	php-common >= 4:5.2.13-10
Requires:	php-mysql
Requires:	php-pcre
Requires:	php-session
Requires:	php-snmp
Requires:	php-xml
Requires:	rrdtool
Requires:	webapps
Requires:	webserver
Requires:	webserver(access)
Requires:	webserver(alias)
Requires:	webserver(indexfile)
Requires:	webserver(php)
Suggests:	cacti-spine
Suggests:	php-gd
Provides:	cacti(pia) = %{pia_ver}
Provides:	user(cacti)
Obsoletes:	cacti-add_template
Obsoletes:	cacti-plugin-update
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		/usr/share/%{name}

%description
Cacti is a complete frondend to rrdtool, it stores all of the
nessesary information to create graphs and populate them with data in
a MySQL database.

The frontend is completely PHP driven. Along with being able to
maintain Graphs, Data Sources, and Round Robin Archives in a database,
cacti handles the data gathering also. There is also SNMP support for
those used to creating traffic graphs with MRTG.

%description -l pl.UTF-8
Cacti to pełny frontend do rrdtoola, zapamiętujący wszystkie
informacje potrzebne do tworzenia wykresów i wypełniające je danymi w
bazie MySQL.

Frontend jest w pełni oparty na PHP. Oprócz zarządzania wykresami,
źródłami danych, archiwami Round Robin w bazie danych, cacti obsługuje
także gromadzenie danych. Ma także obsługę SNMP przydatną przy
tworzeniu wykresów ruchu przy użyciu MRTG.

%package setup
Summary:	Cacti setup package
Summary(pl.UTF-8):	Pakiet do wstępnej konfiguracji Cacti
Group:		Applications/WWW
Requires:	%{name} = %{version}-%{release}
Suggests:	%{name}-doc = %{version}-%{release}

%description setup
Install this package to configure initial Cacti installation. You
should uninstall this package when you're done, as it considered
insecure to keep the setup files in place.

%description setup -l pl.UTF-8
Ten pakiet należy zainstalować, aby wstępnie skonfigurować instalację
Cacti. Po tym pakiet powinien zostać odinstalowany, jako że jego
obecność może być niebezpieczna.

%package doc
Summary:	HTML Documentation for Cacti
Summary(pl.UTF-8):	Dokumentacja do Cacti w formacie HTML
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description doc
HTML Documentation for Cacti.

%description doc -l pl.UTF-8
Dokumentacja do Cacti w formacie HTML.

%prep
%setup -q %{?with_pa:-a8}
# official patches
#%patch10 -p1

%if %{with pa}
%patch0 -p1
# copy images and drop the rest
mv cacti-plugin-arch/files/images/* images
%{__rm} -r cacti-plugin-arch
%endif

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

mkdir -p sql
mv *.sql sql
# you should run this sql if your database contains path to %{_datadir}...
cp -p %{SOURCE5} sql
cp -p %{SOURCE6} sql

%{__rm} -r lib/adodb
%{__rm} log/.htaccess
%{__rm} cli/.htaccess
%{__rm} rra/.htaccess

# must require libs to get fatals on missing files, not include
%{__sed} -i -e '
	s,include(dirname(__FILE__)."/../include/global.php");,require(dirname(__FILE__)."/../include/global.php");,
	s,include_once,require_once,
' cli/*.php

# make sure scripts have php shebang
%{__sed} -i -e '1{
    /bin.php/!i#!%{_bindir}/php
}' scripts/*.php  cli/*.php

chmod a+rx scripts/*.php cli/*.php

find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

# make sure cacti runs out of the box
%{__sed} -i -e 's,new_install,%{version},' sql/cacti.sql

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/%{name},%{_appdir}/{docs,plugins},/etc/{cron.d,logrotate.d},%{_sbindir}}
install -d $RPM_BUILD_ROOT/var/{log,{lib,cache}/%{name}}

cp -p *.php $RPM_BUILD_ROOT%{_appdir}
cp -a cli images include install lib resource scripts sql $RPM_BUILD_ROOT%{_appdir}
cp -a docs/html $RPM_BUILD_ROOT%{_appdir}/docs/html
mv $RPM_BUILD_ROOT{%{_appdir}/poller.php,%{_sbindir}/cacti-poller}

cp -a log $RPM_BUILD_ROOT/var/log/%{name}
install -d $RPM_BUILD_ROOT/var/log/archive/%{name}
cp -a rra $RPM_BUILD_ROOT/var/lib/%{name}

mv $RPM_BUILD_ROOT{%{_appdir}/include,%{_sysconfdir}}/config.php
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/cron.d/%{name}
cp -p %{SOURCE7} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}

cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
cp -p %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%useradd -u 184 -d /var/lib/%{name} -g http -c "Cacti User" cacti

%post
if [ ! -f /var/log/%{name}/cacti.log ]; then
	install -m660 -oroot -ghttp /dev/null /var/log/%{name}/cacti.log
fi

%{_appdir}/cli/upgrade_database.php || :

%postun
if [ "$1" = "0" ]; then
	%userremove cacti
fi

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%triggerpostun -- %{name} < 0.8.7b-9.5
if [ -f /etc/cacti/cacti.cfg.rpmsave ]; then
	cp -f %{_sysconfdir}/config.php{,.rpmnew}
	mv /etc/cacti/cacti.cfg.rpmsave %{_sysconfdir}/config.php
fi

%files
%defattr(644,root,root,755)
%doc docs/CHANGELOG docs/CONTRIB docs/README docs/txt/manual.txt
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config.php
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/cron.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/%{name}
%attr(755,root,root) %{_sbindir}/cacti-poller
%dir %{_appdir}
%exclude %{_appdir}/install
%exclude %{_appdir}/docs
%{_appdir}/resource
%{_appdir}/sql
%{_appdir}/lib
%{_appdir}/include
%{_appdir}/images
%{_appdir}/plugins
%{_appdir}/*.php

%dir %{_appdir}/cli
%attr(755,root,root) %{_appdir}/cli/*

%dir %{_appdir}/scripts
%attr(755,root,root) %{_appdir}/scripts/*

%attr(750,root,http) %dir /var/lib/%{name}
%attr(770,root,http) %dir /var/lib/%{name}/rra
%attr(730,root,http) %dir /var/log/%{name}
%attr(750,root,logs) %dir /var/log/archive/%{name}
%attr(660,root,http) %ghost /var/log/%{name}/cacti.log
%attr(730,root,http) %dir /var/cache/%{name}

%files setup
%defattr(644,root,root,755)
%{_appdir}/install

%files doc
%defattr(644,root,root,755)
%{_appdir}/docs
