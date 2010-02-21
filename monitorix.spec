%define name    monitorix
%define version 1.2.0
%define rel     3
%define release %mkrel %{rel}

Name:           %{name}
Version:        %{version}
Release:        %{release}
Summary: Monitorix is a free, open source, lightweight system monitoring tool
License: GPLv2
Group: Monitoring
URL: http://www.monitorix.org
Source0: http://www.monitorix.org/%{name}-%{version}.tar.gz
Source1: %{name}.initscript
Patch0: monitorix-1.2.0-add_mdv_support.patch
Patch1: monitorix-1.2.0-non_interactive_mode.patch
Patch2: monitorix-1.2.0-relocatable.patch
Patch3: monitorix-1.2.0-use_distro_name.patch
Requires: rrdtool, xinetd, apache, perl-CGI
Requires: iptables
Requires(post):   rpm-helper
Requires(preun):   rpm-helper
%if %mdkversion < 201010
Requires(postun):   rpm-helper
%endif
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}

%description
Monitorix is a free, open source, lightweight system monitoring tool
designed to monitorize as many services as it can. At this time it
monitors from the CPU load and temperatures to the users using the
system. Network devices activity, network services demand and even
the devices' interrupt activity are also monitored. The current
status of any corporate Linux server with Monitorix installed can be
accessed via a web browser.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build

%install
rm -rf ${RPM_BUILD_ROOT}

# Run the built-in install script, patched to support mdv
# It actually fails to install the initscript which is missing
# (mandriva is not supported upstream yet)
./install.sh mandriva ${RPM_BUILD_ROOT}

# install initscript provided with this package
mkdir -p ${RPM_BUILD_ROOT}/%{_initrddir}/
install -m 0755 %{SOURCE1} ${RPM_BUILD_ROOT}/%{_initrddir}/%name

# apache configuration
install -d -m 755 %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/%{name}.conf <<EOF
Alias /%{name} /var/www/%{name}
<Directory /var/www/%{name}>
	Order allow,deny
	Allow from all
</Location>
EOF

%clean
rm -rf %{buildroot}

%post
%_post_service %{name}
%if %mdkversion < 201010
%_post_webapp
%endif

%preun
%_preun_service %{name}

%postun
%if %mdkversion < 201010
%_postun_webapp
%endif

%files
%defattr(-,root, root)
%{_initrddir}/%name
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/%{name}.conf
%attr(755,root,root) %{_sbindir}/%{name}.pl
%defattr(-,root,root)
/var/www/%{name}/logo_top.jpg
/var/www/%{name}/logo_bot_black.png
/var/www/%{name}/logo_bot_white.png
/var/www/%{name}/envelope.png
/var/www/%{name}/monitorixico.png
/var/www/%{name}/%{name}.cgi
%config(noreplace) %{_webappconfdir}/%{name}.conf
/var/lib/%{name}/reports/ca/traffic_report.html
/var/lib/%{name}/reports/ca/traffic_report.sh
/var/lib/%{name}/reports/ca/imgs_email/blank.png
/var/lib/%{name}/reports/ca/imgs_email/logo.jpg
/var/lib/%{name}/reports/ca/imgs_email/signature.png
/var/lib/%{name}/reports/ca/imgs_email/title.jpg
/var/lib/%{name}/reports/en/traffic_report.html
/var/lib/%{name}/reports/en/traffic_report.sh
/var/lib/%{name}/reports/en/imgs_email/blank.png
/var/lib/%{name}/reports/en/imgs_email/logo.jpg
/var/lib/%{name}/reports/en/imgs_email/signature.png
/var/lib/%{name}/reports/en/imgs_email/title.jpg
/var/lib/%{name}/reports/de/imgs_email/blank.png
/var/lib/%{name}/reports/de/imgs_email/logo.jpg
/var/lib/%{name}/reports/de/imgs_email/signature.png
/var/lib/%{name}/reports/de/imgs_email/title.jpg
/var/lib/%{name}/reports/de/traffic_report.html
/var/lib/%{name}/reports/de/traffic_report.sh

%doc COPYING Changes Configuration.help README monitorix-apache.conf

