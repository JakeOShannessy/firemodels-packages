Name:           fds-6.5.2
Version:        6.5.2
Release:        1%{?dist}
Summary:        Fire Dynamics Simulator

License:        PublicDomain
Source0:        https://github.com/firemodels/fds/archive/4e9103f2e61e60eb23eed8ad3397e8ac66e16216.zip
Patch0:         backports.patch
Url:            https://pages.nist.gov/fds-smv

BuildRequires:  intel-hpckit
BuildRequires:  intel-basekit
Requires:       bash
Requires:       intel-oneapi-runtime-libs
Requires:       intel-oneapi-mpi

%description
FDS

%prep
%setup -qcn fds-4e9103f2e61e60eb23eed8ad3397e8ac66e16216
cd fds-4e9103f2e61e60eb23eed8ad3397e8ac66e16216
%patch0 -p1

%global __brp_check_rpaths %{nil}
%global debug_package %{nil}
%build
echo "#!/bin/sh" > fds
echo "source /opt/intel/oneapi/setvars.sh" >> fds
echo "ulimit -s unlimited" >> fds
echo "exec mpiexec -np \$1 %{_bindir}/fds-exec \"\${@:2}\"" >> fds
ls
source /opt/intel/oneapi/setvars.sh
cd fds-FDS%{version}/FDS_Compilation/mpi_intel_linux_64
dir=$(pwd)
target=${dir##*/}
make FCOMPL=mpiifort FOPENMPFLAGS="-qopenmp -qopenmp-link static -liomp5" VPATH="../../FDS_Source" -f ../makefile "$target"


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
install fds-4e9103f2e61e60eb23eed8ad3397e8ac66e16216/FDS_Compilation/mpi_intel_linux_64/fds_impi_intel_linux_64 $RPM_BUILD_ROOT/%{_bindir}/fds-exec-%{version}
install fds $RPM_BUILD_ROOT/%{_bindir}/fds-%{version}

%files
%{_bindir}/fds-%{version}
%{_bindir}/fds-exec-%{version}

%changelog
* Sat Dec 18 2021 admin
-