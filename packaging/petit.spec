# Packs a tree already staged by .github/workflows/packages.yml: petit in
# /usr/lib/petit with bytecode for Python 3.11-3.14, and the launcher.
# Build with: rpmbuild -bb --define "pkg_version X.Y.Z" --define "stage DIR"

Name:           petit
Version:        %{pkg_version}
Release:        1
Summary:        Log analysis for systems administrators
License:        AGPL-3.0-or-later
URL:            https://github.com/crunchtools/petit
BuildArch:      noarch
AutoReqProv:    no
Requires:       (python3 >= 3.11 or python3.14 or python3.13 or python3.12 or python3.11 or python311 or python313)

# The tree is prebuilt, bytecode included: no Python macros may touch it.
%global __os_install_post %{nil}
%global _build_id_links none
%global _binary_payload w9.xzdio
%global _source_payload w9.xzdio

%description
petit detects a log's format, then collapses the repetitive into counts so
the unusual is what you read. It also graphs activity over time. It runs on
any Python 3.11 or newer the system has.

%install
cp -a %{stage}/. %{buildroot}/

%files
%license /usr/share/licenses/petit/COPYING
%doc /usr/share/doc/petit/README.md
%doc /usr/share/doc/petit/CHANGELOG.md
/usr/bin/petit
/usr/lib/petit
