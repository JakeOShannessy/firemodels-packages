%global commit  f7f414800cb6e0829433ad150b0da71d4074ed9d
%global repo    fds-smv_deprecated
%global this_version 6.3.0
%global version_suffix %{this_version}
%global arch_suffix _64
%{!?build_openmpi:%global build_openmpi 0}
%global gnu_string mpi_gnu_linux
%global intel_string mpi_intel_linux
%global this_release 2

#TODO: this isn't as clean as the openmpi version
%global _intelmpi_load \
 . /etc/profile.d/modules.sh; \
 module use /opt/intel/oneapi/modulefiles \
 module load mpi \
 module load compiler \
 module load mkl;
%global _intelmpi_unload \
 . /etc/profile.d/modules.sh; \
 module use /opt/intel/oneapi/modulefiles \
 module unload mkl \
 module unload compiler \
 module unload mpi;

Name:           fds%{version_suffix}
Version:        %{this_version}
Release:        %{this_release}%{?dist}
Summary:        Fire Dynamics Simulator

License:        Public Domain
Source0:        https://github.com/firemodels/%{repo}/archive/%{commit}.zip
Source1:        fds.sh.zip
Patch0:         backports.patch
Patch1:         version.patch
Url:            https://pages.nist.gov/fds-smv

Requires: %{name}-common = %{version}-%{release}

%description
FDS


%package common
Summary:        Fire Dynamics Simulator common files
%description common
FDS common files
Requires:       bash
Requires:       util-linux



%if %{build_openmpi}
%package openmpi
Summary:        Fire Dynamics Simulator with OpenMPI
BuildRequires: openmpi-devel(x86-64)
Requires: openmpi(x86-64)
Requires: %{name}-common = %{version}-%{release}
%description openmpi
FDS with OpenMPI

You will need to load the openmpi-%{_arch} module to setup your path properly.
%endif

%package intelmpi
Summary:        Fire Dynamics Simulator with Intel MPI
BuildRequires:  intel-oneapi-mpi-devel
BuildRequires:  intel-oneapi-mkl-devel
BuildRequires:  intel-oneapi-compiler-fortran
Requires:       intel-oneapi-runtime-libs
Requires:       intel-oneapi-mpi
Requires:       %{name}-common = %{version}-%{release}
%description intelmpi
FDS with IntelMPI


%prep
%setup -qc
%setup -qc -a 1
cd %{repo}-%{commit}
%patch0 -p1
%patch1 -p1

%global __brp_check_rpaths %{nil}
%global debug_package %{nil}

%build

# Build common files
{
    echo "#!/bin/sh"
    echo "PROGRAM_VERSION=%{version}"
    echo "VERSION=latest"
    echo "LIBEXECDIR=%{_libexecdir}/fds"
    cat fds.sh
} > ./fds-script

# Build OpenMPI version
%if %{build_openmpi}
%{_openmpi_load}
pushd %{repo}-%{commit}/FDS_Compilation/%{gnu_string}%{?arch_suffix}
export full_commit=%{commit}
export mpi=openmpi
export compiler=gnu
export commit=${full_commit:0:9}
dir=$(pwd)
target=${dir##*/}
make FCOMPL=mpifort FOPENMPFLAGS="-qopenmp -qopenmp-link static -liomp5" VPATH="../../FDS_Source" -f ../makefile "$target"
popd
%{_openmpi_unload}
%endif

# Build IntelMPI version
%{_intelmpi_load}
pushd %{repo}-%{commit}/FDS_Compilation/%{intel_string}%{?arch_suffix}
export full_commit=%{commit}
export mpi=intelmpi
export compiler=intel
export commit=${full_commit:0:9}
dir=$(pwd)
target=${dir##*/}
make FCOMPL=mpiifort FOPENMPFLAGS="-qopenmp -qopenmp-link static -liomp5" VPATH="../../FDS_Source" -f ../makefile "$target"
popd
%{_intelmpi_unload}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_libexecdir}/fds/%{version}
echo %{buildroot}/%{_bindir}

# Install common
install fds-script %{buildroot}/%{_bindir}/fds-%{version}


# Install OpenMPI version
%if %{build_openmpi}
%{_openmpi_load}
install %{repo}-%{commit}/FDS_Compilation/%{gnu_string}%{?arch_suffix}/fds_%{gnu_string}%{?arch_suffix} %{buildroot}/%{_libexecdir}/fds/%{version}/fds-exec-openmpi
%{_openmpi_unload}
%endif

# Install Intel MPI
%{_intelmpi_load}
install %{repo}-%{commit}/FDS_Compilation/%{intel_string}%{?arch_suffix}/fds_%{intel_string}%{?arch_suffix} %{buildroot}/%{_libexecdir}/fds/%{version}/fds-exec-intelmpi
%{_intelmpi_unload}

%files common
%{_bindir}/fds-%{version}

%if %{build_openmpi}
%files openmpi
%{_libexecdir}/fds/%{version}/fds-exec-openmpi
%endif

%files intelmpi
%{_libexecdir}/fds/%{version}/fds-exec-intelmpi

%changelog
* Tue Nov 15 2022 Jake O'Shannessy <joshannessy@smokecloud.io> - %{version}-2
- Correct embedded version information
* Sat Dec 18 2021 Jake O'Shannessy <joshannessy@smokecloud.io> - %{version}-1
- Initial package
