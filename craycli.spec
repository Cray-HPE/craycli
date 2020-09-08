Name: craycli
License: Cray Software License Agreement
Summary: Cray Command Line Tool
Version: %(cat ./build_version)
Release: %(echo ${BUILD_METADATA})
Vendor: Cray Inc.
Group: Cloud
Source: %{name}-%{version}.tar.gz

%description
A CLI tool to interact with a cray system.

%prep
%setup -q

%build
pyinstaller --clean -y \
    --hidden-import toml \
    --hidden-import ConfigParser \
    --hidden-import boto3 \
    --hidden-import websocket \
    --hidden-import argparse \
    --add-data ../build_version:cray \
    --add-data ../cray/modules:cray/modules \
    -p cray --onefile cray/cli.py -n cray --specpath dist

%install
mkdir -p %{buildroot}%{_bindir}
install -m 755 dist/cray %{buildroot}%{_bindir}/cray

%files
%{_bindir}/cray

%changelog
