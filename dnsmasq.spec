Name:           dnsmasq
Version:        2.30
Release:        2%{?dist}
Summary:        A lightweight DHCP/caching DNS server

Group:          System Environment/Daemons
License:        GPL
URL:            http://www.thekelleys.org.uk/dnsmasq/
Source0:        http://www.thekelleys.org.uk/dnsmasq/%{name}-%{version}.tar.gz
Patch0:         http://beer.tclug.org/fedora-extras/dnsmasq/%{name}-%{version}-fedora-extras.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  dbus-devel

Requires(post):	 /sbin/chkconfig
Requires(post):  /sbin/service
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service

%description
Dnsmasq is lightweight, easy to configure DNS forwarder and DHCP server. 
It is designed to provide DNS and, optionally, DHCP, to a small network. 
It can serve the names of local machines which are not in the global 
DNS. The DHCP server integrates with the DNS server and allows machines 
with DHCP-allocated addresses to appear in the DNS with names configured 
either in each host or in a central configuration file. Dnsmasq supports 
static and dynamic DHCP leases and BOOTP for network booting of diskless 
machines.


%prep
%setup -q
%patch0 -p1

%build
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
# normally i'd do 'make install'...it's a bit messy, though
mkdir -p $RPM_BUILD_ROOT%{_sbindir} $RPM_BUILD_ROOT%{_initrddir} \
	$RPM_BUILD_ROOT%{_mandir}/man8
install src/dnsmasq $RPM_BUILD_ROOT%{_sbindir}/dnsmasq
install dnsmasq.conf.example $RPM_BUILD_ROOT%{_sysconfdir}/dnsmasq.conf
install rpm/dnsmasq.rh $RPM_BUILD_ROOT%{_initrddir}/dnsmasq
install man/dnsmasq.8 $RPM_BUILD_ROOT%{_mandir}/man8/

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add dnsmasq

%preun
if [ $1 = 0 ]; then     # execute this only if we are NOT doing an upgrade
    service dnsmasq stop >/dev/null 2>&1
    /sbin/chkconfig --del dnsmasq
fi

%postun
if [ "$1" -ge "1" ]; then
    service dnsmasq restart >/dev/null 2>&1
fi


%files
%defattr(-,root,root,-)
%doc CHANGELOG COPYING FAQ doc.html setup.html UPGRADING_to_2.0
%config(noreplace) %attr(664,root,root) %{_sysconfdir}/dnsmasq.conf
%{_initrddir}/dnsmasq
%{_sbindir}/dnsmasq
%{_mandir}/man8/dnsmasq*


%changelog
* Mon Apr 24 2006 Patrick Laughton <jima@auroralinux.org> 2.30-2
- Disabled stripping of binary while installing (oops)
- Enabled HAVE_ISC_READER/HAVE_DBUS via patch
- Added BuildReq for dbus-devel

* Mon Apr 24 2006 Patrick Laughton <jima@auroralinux.org> 2.30-1
- Initial Fedora Extras RPM
