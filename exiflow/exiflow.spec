%define name Exiflow
%define version 0.4.5.16
%define unmangled_version 0.4.5.16
%define unmangled_version 0.4.5.16
%define release 1

Summary: A set of tools including a little GUI to provide a complete digital photo workflow for Unixes, using EXIF headers as the central information repository.
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{unmangled_version}.tar.gz
License: GNU General Public License (GPL)
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Ulf Rompe, Sebastian Berthold <exiflow-devel@lists.sourceforge.net>
Url: http://exiflow.org/

%description
A set of tools including a little GUI to provide a complete digital photo workflow for Unixes. EXIF headers are used as the central information repository, so users may change their software at any time without loosing any data. The tools may be used individually or combined.

%prep
%setup -n %{name}-%{unmangled_version} -n %{name}-%{unmangled_version}

%build
python setup.py build

%install
python setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
