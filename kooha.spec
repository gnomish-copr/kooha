Name:           kooha
Version:        2.3.0
Release:        1%{?dist}
Summary:        Elegantly record your screen
License:        GPL-3.0-only
URL:            https://github.com/SeaDve/Kooha
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cargo
BuildRequires:  meson
BuildRequires:  gcc
BuildRequires:  rust-packaging
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1) >= 1.5.0
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  libappstream-glib
BuildRequires:  desktop-file-utils
BuildRequires:  libxcb-devel
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-audio-1.0)
BuildRequires:  pkgconfig(gstreamer-video-1.0)
BuildRequires:  pkgconfig(gstreamer-pbutils-1.0)

# For tests
BuildRequires:  xorg-x11-server-Xvfb

Requires:       gstreamer1-plugins-base
Requires:       gstreamer1-plugins-good
Requires:       gstreamer1-plugins-ugly
Requires:       gstreamer1-vaapi
Requires:       pipewire-gstreamer
Requires:       libadwaita >= 1.5.0
Requires:       x264
Requires:       xdg-desktop-portal

%description
Kooha is a simple screen recorder with a minimal interface.

%prep
%autosetup -n Kooha-%{version}

# Create vendor directory with all dependencies
mkdir -p .cargo
cat > .cargo/config << EOF
[source.crates-io]
registry = "https://github.com/rust-lang/crates.io-index"
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
EOF

# Allow cargo to fetch dependencies online
mkdir -p vendor
cargo vendor vendor

%build
# Disable Cargo's network isolation to allow for dependency fetching
export CARGO_NET_OFFLINE=false
export CARGO_HTTP_DEBUG=false
export CARGO_NET_RETRY=5

%meson
%meson_build

%install
%meson_install

%check
# Tests are currently disabled due to https://github.com/SeaDve/Kooha/issues/197
# xvfb-run meson test -C %{_vpath_builddir} --print-errorlogs

%files
%license COPYING
%doc README.md
%{_bindir}/%{name}
%{_datadir}/applications/io.github.seadve.Kooha.desktop
%{_datadir}/glib-2.0/schemas/io.github.seadve.Kooha.gschema.xml
%{_datadir}/icons/hicolor/*/apps/io.github.seadve.Kooha.*
%{_datadir}/metainfo/io.github.seadve.Kooha.metainfo.xml
%{_datadir}/locale/*/LC_MESSAGES/kooha.mo
%{_datadir}/dbus-1/services/io.github.seadve.Kooha.service
%{_datadir}/icons/hicolor/symbolic/apps/io.github.seadve.Kooha-symbolic.svg
%{_datadir}/kooha/resources.gresource

%changelog
* Sun Apr 13 2025 Taiwbi <taiwbii@proton.me> - 2.3.0-1
- Initial package
