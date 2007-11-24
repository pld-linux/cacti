# TODO
# - patch source to use adodb system path instead of symlinking
# - R: /usr/bin/php should came from rpm autodeps (chmod +x or sth)
%include	/usr/lib/rpm/macros.perl
Summary:	Cacti is a PHP frontend for rrdtool
Summary(pl.UTF-8):	Cacti - frontend w PHP do rrdtoola
Name:		cacti
Version:	0.8.6j
Release:	6
License:	GPL
Group:		Applications/WWW
Source0:	http://www.cacti.net/downloads/%{name}-%{version}.tar.gz
# Source0-md5:	29436be46b289d13dfce48e7618129e2
Patch1:		http://www.cacti.net/downloads/patches/0.8.6j/ping_php_version4_snmpgetnext.patch
Patch2:		http://www.cacti.net/downloads/patches/0.8.6j/tree_console_missing_hosts.patch
Patch3:		http://www.cacti.net/downloads/patches/0.8.6j/thumbnail_graphs_not_working.patch
Patch4:		http://www.cacti.net/downloads/patches/0.8.6j/graph_debug_lockup_fix.patch
Patch5:		http://www.cacti.net/downloads/patches/0.8.6j/snmpwalk_fix.patch
Patch6:		http://www.cacti.net/downloads/patches/0.8.6j/sec_sql_injection-0.8.6j.patch
Patch10:	%{name}-plugin-%{version}.diff
Patch11:	%{name}-config.patch
Patch12:	%{name}-opera.patch
URL:		http://www.cacti.net/
BuildRequires:	rpm-perlprov
Requires:	/usr/bin/php
Requires:	adodb >= 4.67-1.17
Requires:	crondaemon
Requires:	nc
Requires:	net-snmp-utils
Requires:	php(gd)
Requires:	php(mysql)
Requires:	php(pcre)
Requires:	php(snmp)
Requires:	php(xml)
Requires:	rrdtool
Requires:	webserver
Requires:	webserver(php)
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

%description -l pl.UTF-8
Cacti to pełny frontend do rrdtoola, zapamiętujący wszystkie
informacje potrzebne do tworzenia wykresów i wypełniające je danymi
w bazie MySQL.

Frontend jest w pełni oparty na PHP. Oprócz zarządzania wykresami,
źródłami danych, archiwami Round Robin w bazie danych, cacti
obsługuje także gromadzenie danych. Ma także obsługę SNMP
przydatną przy tworzeniu wykresów ruchu przy użyciu MRTG.

%prep
%setup -q
%patch1 -p1
%patch2	-p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1

rm -rf lib/adodb

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{webadminroot}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{%{name},cron.d}
install -d $RPM_BUILD_ROOT/var/{log,lib/%{name}}
cp -aRf * $RPM_BUILD_ROOT%{webadminroot}
ln -s . $RPM_BUILD_ROOT%{webadminroot}/%{name}

# TODO: move this to SOURCES. it's a lot better to backtrack changes
# if it's a separate file.
cat << 'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/%{name}.cfg
<?php
$database_type = 'mysql';
$database_default = 'cacti';
$database_hostname = 'localhost';
$database_username = 'cactiuser';
$database_password = 'cactiuser';

$plugins = array();
// $plugins[] = 'thold';
// $plugins[] = 'monitor';
// $plugins[] = 'discovery';

/* Do not edit this line */
$config = array();

/* This is full URL Path to the Cacti installation
   For example, if your cacti was accessible by http://server/cacti/ you would user '/cacti/'
   as the url path.  For just http://server/ use '/'
*/
$config['url_path'] = '/cacti/';

?>
EOF

mv $RPM_BUILD_ROOT%{webadminroot}/log $RPM_BUILD_ROOT/var/log/%{name}
ln -sf /var/log/cacti $RPM_BUILD_ROOT%{webadminroot}/log

mv $RPM_BUILD_ROOT%{webadminroot}/rra $RPM_BUILD_ROOT/var/lib/%{name}
ln -sf /var/lib/%{name}/rra $RPM_BUILD_ROOT%{webadminroot}/rra
ln -sf %{_datadir}/php/adodb $RPM_BUILD_ROOT%{webadminroot}/lib/adodb

cat  << 'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/cron.d/%{name}
*/5 * * * * http umask 022; %{_bindir}/php %{webadminroot}/poller.php > /dev/null 2>&1
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc docs/CHANGELOG docs/CONTRIB docs/README
%attr(750,root,http) %dir %{_sysconfdir}/%{name}
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/%{name}.cfg
%attr(770,root,http) %dir /var/log/%{name}
%attr(660,root,http) %ghost /var/log/%{name}/*.log
%attr(750,root,http) %dir /var/lib/%{name}
%attr(770,root,http) %dir /var/lib/%{name}/rra
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/cron.d/%{name}
%{webadminroot}
