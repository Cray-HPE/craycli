BuildRequires: systemd-rpm-macros
Name: craycli
License: MIT License
Summary: Cray Command Line Tool
Version: %(cat .version)
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
    --hidden-import configparser \
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
%license LICENSE
%{_bindir}/cray

%changelog
