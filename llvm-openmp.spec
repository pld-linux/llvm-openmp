# TODO: offload library? (requires Intel COI Runtime + Intel MYO Runtime)
#
# Conditional build:
%bcond_without	fortran		# Fortran modules
#
Summary:	Intel OpenMP runtime library implementation for use with Clang
Summary(pl.UTF-8):	Implementacja biblioteki uruchomieniowej OpenMP firmy Intel dla kompilatora Clang
Name:		llvm-openmp
Version:	3.6.0
Release:	1
License:	BSD-like or MIT
Group:		Libraries
Source0:	http://llvm.org/releases/%{version}/openmp-%{version}.src.tar.xz
# Source0-md5:	e681500865e66e285af9cf3f4bfb6cf2
Patch0:		openmp-pld.patch
URL:		http://openmp.llvm.org/
BuildRequires:	cmake >= 2.8
%{?with_fortran:BuildRequires:	gcc-fortran}
BuildRequires:	rpmbuild(macros) >= 1.605
ExclusiveArch:	%{ix86} %{x8664} arm aarch64 ppc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%ifarch %{ix86}
%define		iomp_arch	32
%endif
%ifarch %{x8664}
%define		iomp_arch	32e
%endif
%ifarch arm aarch64 ppc64
%define		iomp_arch	%{_arch}
%endif

%description
The OpenMP subproject of LLVM is intended to contain all of the
components required to build an executing OpenMP program that are
outside the compiler itself. Support for OpenMP 3.1 in Clang is in the
process of being promoted into the Clang mainline, and can be found at
OpenMP/Clang: <http://clang-omp.github.io/>. 

%description -l pl.UTF-8
Podprojekt OpenMP projektu LLVM ma na celu skompletowanie wszystkich
komponentów wymaganych do zbudowania działającego programu OpenMP poza
samym kompilatorem. Obsługa OpenMP 3.1 w Clangu jest w trakcie
włączania do głównej linii kompilatora i można ją znaleźć w
repozytorium OpenMP/Clang: <http://clang-omp.github.io/>. 

%package fortran-devel
Summary:	Fortran modules for Intel OpenMP implementation
Summary(pl.UTF-8):	Moduły Fortranu implementacji OpenMP firmy Intel
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description fortran-devel
Fortran modules for Intel OpenMP implementation.

%description fortran-devel -l pl.UTF-8
Moduły Fortranu implementacji OpenMP firmy Intel.

%prep
%setup -q -n openmp-%{version}.src
%patch0 -p1

%build
cd runtime
install -d build
cd build
%cmake .. \
%ifarch arm ppc64
	-Darch=%{iomp_arch} \
%endif
	%{?with_fortran:-Dcreate_fortran_modules=ON}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_includedir}/iomp,%{_libdir}}

cp -p runtime/exports/common.pld/include/omp_lib.f90 $RPM_BUILD_ROOT%{_includedir}/iomp
cp -p runtime/exports/lin_%{iomp_arch}.pld/include/omp_lib*.mod $RPM_BUILD_ROOT%{_includedir}/iomp
cp -p runtime/exports/lin_%{iomp_arch}.pld/include_compat/iomp_lib.h $RPM_BUILD_ROOT%{_includedir}/iomp
install runtime/exports/lin_%{iomp_arch}.pld/lib/libiomp5.so $RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CREDITS.txt LICENSE.txt www/{README.txt,Reference.pdf,*.{html,css}}
%attr(755,root,root) %{_libdir}/libiomp5.so

%if %{with fortran}
%files fortran-devel
%defattr(644,root,root,755)
%{_includedir}/iomp
%endif
