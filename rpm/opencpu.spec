Name: opencpu
Version: 1.4.3.99
Release: rpm0
Source: %{name}-%{version}.tar.gz
License: Apache2
Summary: The OpenCPU system for embedded scientific computing and reproducible research.
Group: Applications/Internet
Buildroot: %{_tmppath}/%{name}-buildroot
URL: http://www.opencpu.org
BuildRequires: R-devel
BuildRequires: glibc-devel
BuildRequires: libcurl-devel
BuildRequires: protobuf-devel
BuildRequires: make
BuildRequires: texlive-preprint
BuildRequires: texlive-appendix
BuildRequires: texlive-upquote
Requires: opencpu-server

%description
The OpenCPU system exposes an HTTP API for embedded scientific computing with R. This provides reliable and scalable foundations for integrating R based analysis and visualization modules into pipelines, web applications or big data infrastructures. The OpenCPU server can run either as a single-user development server within the interactive R session, or as a high performance multi-user cloud server that builds on Linux, Nginx and rApache.

%package lib
Summary: OpenCPU package library.
Group: Applications/Internet
Requires: R-devel
Requires: make
Requires: wget
Requires: unzip
Requires: libcurl
Requires: protobuf

%description lib
This RPM package contains a frozen library of platform specific builds of R packages required by the OpenCPU system.

%package server
Summary: The OpenCPU API server.
Group: Applications/Internet
Requires: opencpu-lib
Requires: rapache
Requires: mod_ssl
Requires: MTA

%description server
The OpenCPU cloud server builds on R and Apache2 (httpd) to expose the OpenCPU HTTP API.

%prep
%setup

%build
NO_APPARMOR=1 make

%install
# For opencpu-lib:
mkdir -p  %{buildroot}/usr/lib/opencpu/library
cp -Rf opencpu-lib/build/* %{buildroot}/usr/lib/opencpu/library/
# For opencpu-server:
mkdir -p %{buildroot}/etc/httpd/conf.d
mkdir -p %{buildroot}/etc/cron.d
mkdir -p %{buildroot}/usr/lib/opencpu/scripts
mkdir -p %{buildroot}/usr/lib/opencpu/rapache
mkdir -p %{buildroot}/etc/opencpu
mkdir -p %{buildroot}/var/log/opencpu
cp -Rf opencpu-server/sites-available/* %{buildroot}/etc/httpd/conf.d/
cp -Rf opencpu-server/cron.d/* %{buildroot}/etc/cron.d/
cp -Rf opencpu-server/scripts/* %{buildroot}/usr/lib/opencpu/scripts/
cp -Rf opencpu-server/rapache/* %{buildroot}/usr/lib/opencpu/rapache/
cp -Rf opencpu-server/conf/* %{buildroot}/etc/opencpu/
cp -Rf server.conf %{buildroot}/etc/opencpu/

%post server
chmod +x /usr/lib/opencpu/scripts/*.sh
touch /var/log/opencpu/access.log
touch /var/log/opencpu/error.log
setsebool -P httpd_setrlimit=1 httpd_can_network_connect_db=1 httpd_can_network_connect=1 httpd_can_connect_ftp=1 httpd_can_sendmail=1 || true
semanage port -a -t http_port_t -p tcp 8004 || true

%postun server
userdel opencpu || true
apachectl restart || true
rm -Rf /etc/opencpu
rm -Rf /usr/lib/opencpu
rm -Rf /var/log/opencpu

%files lib
/usr/lib/opencpu/library

%files server
/etc/opencpu
/usr/lib/opencpu/scripts
/usr/lib/opencpu/rapache
/etc/cron.d
/etc/httpd/conf.d
%dir /var/log/opencpu