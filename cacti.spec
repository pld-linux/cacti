%include	/usr/lib/rpm/macros.perl
Summary:	Cacti is a PHP frontend for rrdtool
Summary(pl):	Cacti - frontend w PHP do rrdtoola
Name:		cacti
Version:	0.8.6h
Release:	1
License:	GPL
Group:		Applications/WWW
Source0:	http://www.cacti.net/downloads/%{name}-%{version}.tar.gz
# Source0-md5:	5f6100b525b5b29e81f43cc7c55f4000
Patch0:		http://www.cacti.net/downloads/patches/0.8.6h/fix_search_session_clear_issue.patch
Patch1:		http://www.cacti.net/downloads/patches/0.8.6h/fix_sql_syntax_related_to_default_rra_id.patch
Patch2:		http://www.cacti.net/downloads/patches/0.8.6h/nth_percentile_empty_return_set_issue.patch
Patch3:		http://www.cacti.net/downloads/patches/0.8.6h/mysql_5x_strict.patch
Patch4:         %{name}-plugin-%{version}.diff
Patch5:		%{name}-config.patch
URL:		http://www.cacti.net/
BuildRequires:	rpm-perlprov
Requires:	crondaemon
Requires:	net-snmp-utils
Requires:	php
Requires:	php-cli
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
Cacti to pe�ny frontend do rrdtoola, zapami�tuj�cy wszystkie
informacje potrzebne do tworzenia wykres�w i wype�niaj�ce je danymi w
bazie MySQL.

Frontend jest w pe�ni oparty na PHP. Opr�cz zarz�dzania wykresami,
�r�d�ami danych, archiwami Round Robin w bazie danych, cacti obs�uguje
tak�e gromadzenie danych. Ma tak�e obs�ug� SNMP przydatn� przy
tworzeniu wykres�w ruchu przy u�yciu MRTG.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build

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

cat  << 'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/cron.d/%{name}
*/5 * * * * http umask 022; /usr/bin/php %{webadminroot}/poller.php > /dev/null 2>&1
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
