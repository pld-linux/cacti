# TODO
# - patch source to use adodb system path instead of symlinking
%include	/usr/lib/rpm/macros.perl
Summary:	Cacti is a PHP frontend for rrdtool
Summary(pl):	Cacti - frontend w PHP do rrdtoola
Name:		cacti
Version:	0.8.6j
Release:	1
License:	GPL
Group:		Applications/WWW
Source0:	http://www.cacti.net/downloads/%{name}-%{version}.tar.gz
# Source0-md5:	29436be46b289d13dfce48e7618129e2
Patch10:	%{name}-plugin-%{version}.diff
Patch11:	%{name}-config.patch
URL:		http://www.cacti.net/
BuildRequires:	rpm-perlprov
Requires:	adodb >= 4.67-1.17
Requires:	crondaemon
Requires:	net-snmp-utils
Requires:	php(gd)
Requires:	php(mysql)
Requires:	php(pcre)
Requires:	php(snmp)
Requires:	php(xml)
Requires:	php-cli
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
%patch10 -p1
%patch11 -p1

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
ln -sf /usr/share/php/adodb $RPM_BUILD_ROOT%{webadminroot}/lib/adodb

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
