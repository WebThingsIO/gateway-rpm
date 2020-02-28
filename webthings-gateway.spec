Name: webthings-gateway
Version: 0.11.0
Release: 1%{?dist}
Summary: WebThings Gateway by Mozilla

License: MPL-2.0
URL: https://iot.mozilla.org/gateway/

BuildRequires: autoconf automake nodejs npm git python python3 python3-pip python3-setuptools nanomsg-devel libffi-devel python3-devel gcc gcc-c++ systemd make zlib-devel libpng-devel
Requires: {{nodejs}} {{python3}} python3-pip nanomsg libffi pagekite
Requires(pre): shadow-utils

Source0: %{name}_0.11.0.orig.tar.gz
Source1: %{name}.service
Source2: %{name}-intent-parser.service

Patch0: fix-config.patch
Patch1: add-launcher.patch

%description
Web of Things gateway, created by Mozilla, which can bridge existing
Internet of Things (IoT) devices to the web.

%define debug_package %{nil}

%prep
%autosetup -n %{name} -p1

%build
NPM_CACHE=$(mktemp -dq)
CPPFLAGS="-DPNG_ARM_NEON_OPT=0" npm --cache "${NPM_CACHE}" ci
./node_modules/.bin/webpack
npm --cache "${NPM_CACHE}" prune --production
rm -rf "${NPM_CACHE}"
# clean up node modules to prevent broken and unnecessary dependencies
rm -rf ./node_modules/performance-now/test/
rm -rf ./node_modules/nanomsg/test/
chmod a+x %{name}
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
mkdir -p %{buildroot}/opt/%{name}
mkdir -p %{buildroot}/opt/%{name}/config
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_unitdir}
cp -r build %{buildroot}/opt/%{name}
cp config/default.js %{buildroot}/opt/%{name}/config
cp -r intent-parser %{buildroot}/opt/%{name}
cp -r node_modules %{buildroot}/opt/%{name}
cp package-lock.json %{buildroot}/opt/%{name}
cp package.json %{buildroot}/opt/%{name}
cp -r python %{buildroot}/opt/%{name}
cp -r src %{buildroot}/opt/%{name}
cp -r static %{buildroot}/opt/%{name}
cp %{name} %{buildroot}%{_bindir}
cp %{SOURCE1} %{buildroot}%{_unitdir}
cp %{SOURCE2} %{buildroot}%{_unitdir}

%pre
getent group webthings >/dev/null || groupadd -f -r webthings
if ! getent passwd webthings > /dev/null ; then
  useradd -r -l -g webthings -d /var/run/%{name} -s /sbin/nologin -c "Mozilla WebThings Gateway" webthings
fi

%post
if [ $1 -eq 1 ] && [ -x /usr/bin/systemctl ] ; then
  # Initial installation
  systemctl enable %{name}-intent-parser.service %{name}.service || :
  systemctl start %{name}-intent-parser.service %{name}.service || :
fi

%preun
if [ $1 -eq 0 ] && [ -x /usr/bin/systemctl ] ; then
  # Package removal, not upgrade
  systemctl --no-reload disable --now %{name}.service %{name}-intent-parser.service || :
fi

%postun
if [ $1 -ge 1 ] && [ -x /usr/bin/systemctl ] ; then
  # Package upgrade, not uninstall
  systemctl try-restart %{name}-intent-parser.service %{name}.service || :
fi

%files
%license LICENSE
%dir /opt/%{name}/
/opt/%{name}/*
%{_bindir}/%{name}
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}-intent-parser.service

%changelog
* Mon Dec 16 2019 Michael Stegeman <mstegeman@mozilla.com>
- First webthings-gateway package.
