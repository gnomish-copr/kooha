Name:           kooha
Version:        2.3.0
Release:        1%{?dist}
Summary:        Elegantly record your screen
License:        GPL-3.0-only
URL:            https://github.com/SeaDve/Kooha
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cargo
BuildRequires:  rust
BuildRequires:  clippy
BuildRequires:  meson
BuildRequires:  pango-devel
BuildRequires:  gcc
BuildRequires:  gtk4-devel
BuildRequires:  libadwaita-devel
BuildRequires:  glib2-devel
BuildRequires:  gstreamer1-devel
BuildRequires:  gstreamer1-plugins-base-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib-devel
BuildRequires:  gettext

Requires:       glib2
Requires:       pipewire-gstreamer
Requires:       gstreamer1-plugins-base
Requires:       gstreamer1-plugins-good
Requires:       gstreamer1-plugins-ugly
Requires:       gstreamer1-vaapi
Requires:       gtk4
Requires:       libadwaita
Requires:       pulseaudio-libs
Requires:       x264
Requires:       xdg-desktop-portal

%description
Kooha is a simple screen recorder with a minimal interface. 

%prep
%autosetup -n Kooha-%{version}

# Prevent network access during build
mkdir -p .cargo
cat > .cargo/config.toml << EOF
[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
EOF

%if ! %{defined _no_cargo_vendor}
mkdir vendor
cargo vendor > /dev/null
%endif

%build
%meson
%meson_build

%check
# Tests are disabled due to issue #197
# https://github.com/SeaDve/Kooha/issues/197
# %meson_test

%install
%meson_install

%files
%license COPYING
%doc README.md
%{_bindir}/io.github.seadve.Kooha
%{_datadir}/applications/io.github.seadve.Kooha.desktop
%{_datadir}/glib-2.0/schemas/io.github.seadve.Kooha.gschema.xml
%{_datadir}/icons/hicolor/*/apps/io.github.seadve.Kooha*
%{_datadir}/metainfo/io.github.seadve.Kooha.metainfo.xml
%{_datadir}/locale/*/LC_MESSAGES/io.github.seadve.Kooha.mo

%changelog
* Tue Apr 08 2025 Taiwbi <taiwbii@proton.me> - 2.3.0-1
- Initial package
