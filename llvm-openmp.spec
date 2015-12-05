# TODO: offload library? (requires Intel COI Runtime + Intel MYO Runtime)
#
# Conditional build:
%bcond_without	fortran		# Fortran modules
#
Summary:	Intel OpenMP runtime library implementation for use with Clang
Summary(pl.UTF-8):	Implementacja biblioteki uruchomieniowej OpenMP firmy Intel dla kompilatora Clang
Name:		llvm-openmp
Version:	3.7.0
Release:	1
License:	BSD-like or MIT
Group:		Libraries
Source0:	http://llvm.org/releases/%{version}/openmp-%{version}.src.tar.xz
# Source0-md5:	f482c86fdead50ba246a1a2b0bbf206f
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

%package devel
Summary:	Header file for Intel OpenMP implementation
Summary(pl.UTF-8):	Plik nagłówkowy implementacji OpenMP firmy Intel
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header file for Intel OpenMP implementation.

%description devel -l pl.UTF-8
Plik nagłówkowy implementacji OpenMP firmy Intel.

%package fortran-devel
Summary:	Fortran modules for Intel OpenMP implementation
Summary(pl.UTF-8):	Moduły Fortranu implementacji OpenMP firmy Intel
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description fortran-devel
Fortran modules for Intel OpenMP implementation.

%description fortran-devel -l pl.UTF-8
Moduły Fortranu implementacji OpenMP firmy Intel.

%prep
%setup -q -n openmp-%{version}.src

%build
cd runtime
install -d build
cd build
libsubdir=%{_lib}
%cmake .. \
%ifarch arm ppc64
	-DLIBOMP_ARCH=%{iomp_arch} \
%endif
	-DLIBOMP_LIBDIR_SUFFIX="${libsuffix#lib}" \
	%{?with_fortran:-DLIBOMP_FORTRAN_MODULES=ON}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_includedir}/iomp,%{_libdir}}

cp -p runtime/exports/common/include/*.h $RPM_BUILD_ROOT%{_includedir}/iomp
%if %{with fortran}
cp -p runtime/exports/lin_%{iomp_arch}/include_compat/*.mod $RPM_BUILD_ROOT%{_includedir}/iomp
%endif
install runtime/exports/lin_%{iomp_arch}/lib/libomp.so $RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CREDITS.txt LICENSE.txt www/{README.txt,Reference.pdf,*.{html,css}}
%attr(755,root,root) %{_libdir}/libomp.so

%files devel
%defattr(644,root,root,755)
%dir %{_includedir}/iomp
%{_includedir}/iomp/omp.h

%if %{with fortran}
%files fortran-devel
%defattr(644,root,root,755)
%{_includedir}/iomp/omp_lib.h
%{_includedir}/iomp/omp_lib.mod
%{_includedir}/iomp/omp_lib_kinds.mod
%endif
