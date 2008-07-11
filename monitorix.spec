Summary: Monitorix rrd graph System status monitor
Name: monitorix
Version: 1.2.0
Release: %mkrel 1
License: GPL
Group: Monitoring
URL: http://www.monitorix.org

Source: %{name}-%{version}.tar.gz
Requires: bash, rrdtool, perl, xinetd, apache, perl-CGI
Requires: iptables
BuildRoot:      %{_tmppath}/%{name}-%{version}
BuildArch: noarch

%description
System status monitor for kernels 2.4 and 2.6.

%prep
%setup -q

%build

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}/%{_initrddir}/
install -m 0755 monitorix.init ${RPM_BUILD_ROOT}/%{_initrddir}/%name
mkdir -p ${RPM_BUILD_ROOT}/%{_sysconfdir}/%name
install -m 0644 monitorix.conf ${RPM_BUILD_ROOT}/%{_sysconfdir}/%name/%{name}.conf
mkdir -p ${RPM_BUILD_ROOT}/%{_sysconfdir}/cron.d
install -m 0644 monitorix.sh ${RPM_BUILD_ROOT}/%{_sysconfdir}/cron.d/%name
mkdir -p ${RPM_BUILD_ROOT}/%{_sbindir}
install -m 0755 monitorix.pl ${RPM_BUILD_ROOT}/%{_sbindir}/
mkdir -p ${RPM_BUILD_ROOT}/var/www/html/%name
install -m 0644 logo_top.jpg ${RPM_BUILD_ROOT}/var/www/html/%name
install -m 0644 logo_bot.jpg ${RPM_BUILD_ROOT}/var/www/html/%name
install -m 0644 envelope.png ${RPM_BUILD_ROOT}/var/www/html/%name
mkdir -p ${RPM_BUILD_ROOT}/var/www/html/%name/imgs
mkdir -p ${RPM_BUILD_ROOT}/var/www/cgi-bin/%name
install -m 0755 monitorix.cgi ${RPM_BUILD_ROOT}/var/www/cgi-bin
install -m 0755 localhost.cgi ${RPM_BUILD_ROOT}/var/www/cgi-bin/%name
mkdir -p ${RPM_BUILD_ROOT}/var/lib/%name/reports/ca/imgs_email
install -m 0644 reports/ca/traffic_report.html ${RPM_BUILD_ROOT}/var/lib/%name/reports/ca
install -m 0755 reports/ca/traffic_report.sh ${RPM_BUILD_ROOT}/var/lib/%name/reports/ca
install -m 0644 reports/ca/imgs_email/blank.png ${RPM_BUILD_ROOT}/var/lib/%name/reports/ca/imgs_email
install -m 0644 reports/ca/imgs_email/logo.jpg ${RPM_BUILD_ROOT}/var/lib/%name/reports/ca/imgs_email
install -m 0644 reports/ca/imgs_email/signature.png ${RPM_BUILD_ROOT}/var/lib/%name/reports/ca/imgs_email
install -m 0644 reports/ca/imgs_email/title.jpg ${RPM_BUILD_ROOT}/var/lib/%name/reports/ca/imgs_email
mkdir -p ${RPM_BUILD_ROOT}/var/lib/%name/reports/en/imgs_email
install -m 0644 reports/en/traffic_report.html ${RPM_BUILD_ROOT}/var/lib/%name/reports/en
install -m 0755 reports/en/traffic_report.sh ${RPM_BUILD_ROOT}/var/lib/%name/reports/en
install -m 0644 reports/en/imgs_email/blank.png ${RPM_BUILD_ROOT}/var/lib/%name/reports/en/imgs_email
install -m 0644 reports/en/imgs_email/logo.jpg ${RPM_BUILD_ROOT}/var/lib/%name/reports/en/imgs_email
install -m 0644 reports/en/imgs_email/signature.png ${RPM_BUILD_ROOT}/var/lib/%name/reports/en/imgs_email
install -m 0644 reports/en/imgs_email/title.jpg ${RPM_BUILD_ROOT}/var/lib/%name/reports/en/imgs_email
mkdir -p ${RPM_BUILD_ROOT}/var/lib/%name/usage

%clean
rm -rf $RPM_BUILD_ROOT

%post
chkconfig --add %name
mkdir -p /var/www/html/%name/imgs
mkdir -p /var/lib/%name/usage
chown apache:apache /var/www/html/%name/imgs
mv %{_sysconfdir}/cron.d/%name %{_sysconfdir}/cron.d/.%name

%files
%defattr(-,root, root)
%{_initrddir}/%name
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/%name/%{name}.conf
%attr(755,root,root) %config(noreplace) %{_sysconfdir}/cron.d/%{name}
%attr(755,root,root) %{_sbindir}/%{name}.pl
%defattr(-,root,root)
/var/www/html/%{name}/logo_top.jpg
/var/www/html/%{name}/logo_bot.jpg
/var/www/html/%{name}/envelope.png
/var/www/cgi-bin/%{name}.cgi
/var/www/cgi-bin/%{name}/localhost.cgi
%config(noreplace) /var/lib/%{name}/reports/ca/traffic_report.html
%config(noreplace) /var/lib/%{name}/reports/ca/traffic_report.sh
%config(noreplace) /var/lib/%{name}/reports/ca/imgs_email/blank.png
%config(noreplace) /var/lib/%{name}/reports/ca/imgs_email/logo.jpg
%config(noreplace) /var/lib/%{name}/reports/ca/imgs_email/signature.png
%config(noreplace) /var/lib/%{name}/reports/ca/imgs_email/title.jpg
%config(noreplace) /var/lib/%{name}/reports/en/traffic_report.html
%config(noreplace) /var/lib/%{name}/reports/en/traffic_report.sh
%config(noreplace) /var/lib/%{name}/reports/en/imgs_email/blank.png
%config(noreplace) /var/lib/%{name}/reports/en/imgs_email/logo.jpg
%config(noreplace) /var/lib/%{name}/reports/en/imgs_email/signature.png
%config(noreplace) /var/lib/%{name}/reports/en/imgs_email/title.jpg
%doc COPYING Changelog Configuration.help README monitorix-apache.conf
