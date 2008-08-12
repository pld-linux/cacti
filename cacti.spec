# TODO
# - patch source to use adodb system path instead of symlinking
# - shouldn't files in scripts dir be executable?
%include	/usr/lib/rpm/macros.perl
Summary:	Cacti is a PHP frontend for rrdtool
Summary(pl.UTF-8):	Cacti - frontend w PHP do rrdtoola
Name:		cacti
Version:	0.8.7b
Release:	8
License:	GPL
Group:		Applications/WWW
Source0:	http://www.cacti.net/downloads/%{name}-%{version}.tar.gz
# Source0-md5:	63ffca5735b60bc33c68bc880f0e8042
Source1:	%{name}.cfg.php
Source2:	%{name}.crontab
Source3:	http://cactiusers.org/downloads/cacti-plugin-arch.tar.gz
# Source3-md5:	7079c1f366e8ea1b26c7e251e6373226
Patch1:		%{name}-upgrade_from_086k_fix.patch
Patch2:		http://www.cacti.net/downloads/patches/0.8.7b/snmp_auth_none_notice.patch
Patch3:		http://www.cacti.net/downloads/patches/0.8.7b/reset_each_patch.patch
Patch11:	%{name}-config.patch
Patch12:	%{name}-adodb.patch
URL:		http://www.cacti.net/
BuildRequires:	rpm-perlprov
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
Requires:	php(snmp)
Requires:	php(xml)
Requires:	php-cli
Requires:	rrdtool
Requires:	webserver
Requires:	webserver(php)
Suggests:	cacti-spine
Provides:	user(cacti)
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
informacje potrzebne do tworzenia wykresów i wypełniające je danymi w
bazie MySQL.

Frontend jest w pełni oparty na PHP. Oprócz zarządzania wykresami,
źródłami danych, archiwami Round Robin w bazie danych, cacti obsługuje
także gromadzenie danych. Ma także obsługę SNMP przydatną przy
tworzeniu wykresów ruchu przy użyciu MRTG.

%prep
%setup -q -a 3
%patch1 -p1
%patch2 -p1
%patch3 -p1

patch -p1 -s < cacti-plugin-arch/cacti-plugin-0.8.7b-PA-v2.1.diff || exit 1

%patch11 -p1
%patch12 -p1

rm -rf lib/adodb

find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{webadminroot}
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/%{name},/etc/cron.d}
install -d $RPM_BUILD_ROOT/var/{log,lib/%{name}}
cp -a * $RPM_BUILD_ROOT%{webadminroot}
# wtf is this?
ln -s . $RPM_BUILD_ROOT%{webadminroot}/%{name}

cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/%{name}.cfg

mv $RPM_BUILD_ROOT%{webadminroot}/log $RPM_BUILD_ROOT/var/log/%{name}
ln -sf /var/log/cacti $RPM_BUILD_ROOT%{webadminroot}/log

mv $RPM_BUILD_ROOT%{webadminroot}/rra $RPM_BUILD_ROOT/var/lib/%{name}
ln -sf /var/lib/%{name}/rra $RPM_BUILD_ROOT%{webadminroot}/rra
ln -sf %{_datadir}/php/adodb $RPM_BUILD_ROOT%{webadminroot}/lib/adodb

# TODO: switch to user cacti here
cp -a %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/cron.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%useradd -u 184 -d /var/lib/%{name} -g http -c "Cacti User" cacti

%postun
if [ "$1" = "0" ]; then
	%userremove cacti
fi

%files
%defattr(644,root,root,755)
%doc docs/CHANGELOG docs/CONTRIB docs/README cacti-plugin-arch/pa.sql
%attr(750,root,http) %dir %{_sysconfdir}/%{name}
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/%{name}.cfg
%attr(770,root,http) %dir /var/log/%{name}
%attr(660,root,http) %ghost /var/log/%{name}/*.log
%attr(750,root,http) %dir /var/lib/%{name}
%attr(770,root,http) %dir /var/lib/%{name}/rra
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/cron.d/%{name}
%{webadminroot}
