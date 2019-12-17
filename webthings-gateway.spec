Name: webthings-gateway
Version: 0.10.0
Release: 1%{?dist}
Summary: WebThings Gateway by Mozilla

License: MPL-2.0
URL: https://iot.mozilla.org/gateway/

BuildRequires: nodejs npm git python python3 python3-pip python3-setuptools nanomsg-devel libffi-devel python3-devel gcc gcc-c++ systemd
Requires: nodejs python3 python3-pip nanomsg libffi pagekite
Requires(pre): shadow-utils

Source0: webthings-gateway_0.10.0.orig.tar.gz
Source1: webthings-gateway.service
Source2: webthings-gateway-intent-parser.service

Patch0: fix-config.patch
Patch1: add-launcher.patch

%description
Web of Things gateway, created by Mozilla, which can bridge existing
Internet of Things (IoT) devices to the web.

%define debug_package %{nil}

%prep
%autosetup -n webthings-gateway -p1

%build
NPM_CACHE=$(mktemp -dq)
rm -rf ./node_modules package-lock.json
npm --cache "${NPM_CACHE}" install
./node_modules/.bin/webpack
npm --cache "${NPM_CACHE}" prune --production
rm -rf "${NPM_CACHE}"
chmod a+x webthings-gateway
mkdir python
python3 -m pip install \
  --install-option="--prefix=" \
  --no-binary=:all: \
  -t ./python \
  ./gateway-addon-python
python3 -m pip install \
  --install-option="--prefix=" \
  --no-binary=:all: \
  -t ./python \
  adapt-parser==0.3.4

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/opt/webthings-gateway
mkdir -p %{buildroot}/opt/webthings-gateway/config
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_unitdir}
cp -r build %{buildroot}/opt/webthings-gateway
cp config/default.js %{buildroot}/opt/webthings-gateway/config
cp -r intent-parser %{buildroot}/opt/webthings-gateway
cp -r node_modules %{buildroot}/opt/webthings-gateway
cp package-lock.json %{buildroot}/opt/webthings-gateway
cp package.json %{buildroot}/opt/webthings-gateway
cp -r python %{buildroot}/opt/webthings-gateway
cp -r src %{buildroot}/opt/webthings-gateway
cp -r static %{buildroot}/opt/webthings-gateway
cp webthings-gateway %{buildroot}%{_bindir}
cp %{SOURCE1} %{buildroot}%{_unitdir}
cp %{SOURCE2} %{buildroot}%{_unitdir}

%pre
getent group webthings >/dev/null || groupadd -f -r webthings
if ! getent passwd webthings > /dev/null ; then
  useradd -r -l -g webthings -d /var/run/webthings-gateway -s /sbin/nologin -c "Mozilla WebThings Gateway" webthings
fi

%post
if [ $1 -eq 1 ] && [ -x /usr/bin/systemctl ] ; then
  # Initial installation
  systemctl enable webthings-gateway-intent-parser.service webthings-gateway.service || :
  systemctl start webthings-gateway-intent-parser.service webthings-gateway.service || :
fi

%preun
if [ $1 -eq 0 ] && [ -x /usr/bin/systemctl ] ; then
  # Package removal, not upgrade
  systemctl --no-reload disable --now webthings-gateway.service webthings-gateway-intent-parser.service || :
fi

%postun
if [ $1 -ge 1 ] && [ -x /usr/bin/systemctl ] ; then
  # Package upgrade, not uninstall
  systemctl try-restart webthings-gateway-intent-parser.service webthings-gateway.service || :
fi

%files
%license LICENSE
%dir /opt/webthings-gateway/
/opt/webthings-gateway/*
%{_bindir}/webthings-gateway
%{_unitdir}/webthings-gateway.service
%{_unitdir}/webthings-gateway-intent-parser.service

%changelog
* Mon Dec 16 2019 Michael Stegeman <mstegeman@mozilla.com>
- First webthings-gateway package.
