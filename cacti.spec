%include	/usr/lib/rpm/macros.perl
Summary:	Cacti is a PHP frontend for rrdtool
Summary(pl.UTF-8):	Cacti - frontend w PHP do rrdtoola
Name:		cacti
Version:	0.8.7e
Release:	8
License:	GPL
Group:		Applications/WWW
Source0:	http://www.cacti.net/downloads/%{name}-%{version}.tar.gz
# Source0-md5:	7563a58a57d2c6cc0da28cc341a30969
Source1:	%{name}.cfg.php
Source2:	%{name}.crontab
Source3:	%{name}-apache.conf
Source4:	%{name}-lighttpd.conf
Source5:	%{name}-rrdpath.sql
Source6:	%{name}-pa.sql
Patch100:	http://www.cacti.net/downloads/patches/0.8.7e/cli_add_graph.patch
Patch101:	http://www.cacti.net/downloads/patches/0.8.7e/snmp_invalid_response.patch
Patch102:	http://www.cacti.net/downloads/patches/0.8.7e/template_duplication.patch
Patch103:	http://www.cacti.net/downloads/patches/0.8.7e/fix_icmp_on_windows_iis_servers.patch
Patch104:	http://www.cacti.net/downloads/patches/0.8.7e/cross_site_fix.patch
# http://cactiusers.org/wiki/PluginArchitectureInstall
# http://mirror.cactiusers.org/downloads/plugins/cacti-plugin-0.8.7e-PA-v2.6.zip
Patch0:		%{name}-PA.patch
Patch1:		%{name}-config.patch
Patch2:		%{name}-adodb.patch
Patch3:		%{name}-ioerror.patch
Patch4:		%{name}-webroot.patch
Patch5:		%{name}-linux_memory.patch
Patch6:		%{name}-log-verbosity.patch
Patch7:		%{name}-ss_disk-array-indices.patch
Patch8:		%{name}-rrdresourcecheck.patch
Patch9:		host_name-url.patch
Patch10:	cli-relpath.patch
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
Requires:	php(gd)
Requires:	php(mysql)
Requires:	php(pcre)
Requires:	php(session)
Requires:	php(snmp)
Requires:	php(xml)
Requires:	php-cli
Requires:	rrdtool
Requires:	webapps
Requires:	webserver
Requires:	webserver(access)
Requires:	webserver(alias)
Requires:	webserver(indexfile)
Requires:	webserver(php)
Suggests:	cacti-spine
Provides:	user(cacti)
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
%setup -q
%patch100 -p1
%patch101 -p1
%patch102 -p1
%patch103 -p1
%patch104 -p1
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1

mkdir -p sql
mv *.sql sql
# you should run this sql if your database contains path to %{_datadir}...
cp %{SOURCE5} sql
cp %{SOURCE6} sql

rm -rf cacti-plugin-arch
rm -rf lib/adodb
rm -f log/.htaccess
rm -f cli/.htaccess
rm -f rra/.placeholder

# make sure scripts have php shebang
%{__sed} -i -e '1{
    /bin.php/!i#!%{_bindir}/php
}' scripts/*.php  cli/*.php

chmod a+rx scripts/*.php cli/*.php

find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

rm log/.placeholder

# make sure cacti runs out of the box
sed -e "s,new_install,%{version}," -i sql/cacti.sql

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/%{name},%{_appdir}/{docs,plugins},/etc/cron.d,%{_sbindir}}
install -d $RPM_BUILD_ROOT/var/{log,lib/%{name}}

cp -a *.php $RPM_BUILD_ROOT%{_appdir}
cp -a cli images include install lib resource scripts sql $RPM_BUILD_ROOT%{_appdir}
cp -a docs/html $RPM_BUILD_ROOT%{_appdir}/docs/html
mv $RPM_BUILD_ROOT{%{_appdir}/poller.php,%{_sbindir}/cacti-poller}

cp -a log $RPM_BUILD_ROOT/var/log/%{name}
cp -a rra $RPM_BUILD_ROOT/var/lib/%{name}

cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/config.php
cp -a %{SOURCE2} $RPM_BUILD_ROOT/etc/cron.d/%{name}

cp -a %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -a %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
cp -a %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%useradd -u 184 -d /var/lib/%{name} -g http -c "Cacti User" cacti

%post
if [ ! -f /var/log/%{name}/cacti.log ]; then
	install -m660 -oroot -ghttp /dev/null /var/log/%{name}/cacti.log
fi

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
%attr(660,root,http) %ghost /var/log/%{name}/cacti.log

%files setup
%defattr(644,root,root,755)
%{_appdir}/install

%files doc
%defattr(644,root,root,755)
%{_appdir}/docs
