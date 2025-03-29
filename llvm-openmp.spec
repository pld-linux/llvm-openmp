# TODO: offload library? (requires Intel COI Runtime + Intel MYO Runtime)
#
# Conditional build:
%bcond_without	fortran		# Fortran modules
#
Summary:	Intel OpenMP runtime library implementation for use with Clang
Summary(pl.UTF-8):	Implementacja biblioteki uruchomieniowej OpenMP firmy Intel dla kompilatora Clang
Name:		llvm-openmp
Version:	17.0.4
Release:	1
License:	BSD-like or MIT (OMP), Apache v2.0 (Archer)
Group:		Libraries
#Source0Download: https://github.com/llvm/llvm-project/releases/
Source0:	https://github.com/llvm/llvm-project/releases/download/llvmorg-%{version}/openmp-%{version}.src.tar.xz
# Source0-md5:	1581d82df3a5c2dfb9c010c06ca7b9e0
#Source1Download: https://github.com/llvm/llvm-project/releases/
Source1:	https://github.com/llvm/llvm-project/releases/download/llvmorg-%{version}/cmake-%{version}.src.tar.xz
# Source1-md5:	38ae9cc0950f277c8f88e570c4d18010
Patch0:		openmp-x86.patch
URL:		https://openmp.llvm.org/
BuildRequires:	cmake >= 3.20.0
%{?with_fortran:BuildRequires:	gcc-fortran}
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
ExclusiveArch:	%{ix86} %{x8664} %{arm} aarch64 ppc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%ifarch %{ix86}
%define		iomp_arch	32
%endif
%ifarch %{x8664}
%define		iomp_arch	32e
%endif
%ifarch %{arm} aarch64 ppc64
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

%package gdb
Summary:	GDB support for LLVM OpenMP
Summary(pl.UTF-8):	Obsługa GDB do LLVM OpenMP
Group:		Development/Tools
Requires:	%{name}-devel = %{version}-%{release}
Requires:	gdb

%description gdb
GDB support for LLVM OpenMP.

%description gdb -l pl.UTF-8
Obsługa GDB do LLVM OpenMP.

%prep
%setup -q -c -a1
%{__mv} openmp-%{version}.src openmp
%{__mv} cmake-%{version}.src cmake
cd openmp
%patch -P0 -p1

%build
libsubdir=%{_lib}
%cmake -B build openmp \
%ifarch %{arm} ppc64
	-DLIBOMP_ARCH=%{iomp_arch} \
%endif
	-DLIBOMP_LIBDIR_SUFFIX="${libsuffix#lib}" \
	%{?with_fortran:-DLIBOMP_FORTRAN_MODULES=ON}
# -DLLVM_ENABLE_SPHINX=ON needs llvm sources

%{__make} -C build

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# libgomp dropin symlink, but PLD ships original libgomp
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libgomp.so

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc openmp/{CREDITS.txt,LICENSE.TXT,README.rst} openmp/docs/ReleaseNotes.rst
%attr(755,root,root) %{_libdir}/libarcher.so
%attr(755,root,root) %{_libdir}/libomp.so
%attr(755,root,root) %{_libdir}/libompd.so
%ifarch %{x8664} aarch64 ppc64
%attr(755,root,root) %{_libdir}/libomptarget.so
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libiomp5.so
%{_libdir}/libarcher_static.a
%{_includedir}/omp.h
%{_includedir}/omp-tools.h
%{_includedir}/ompt.h
%{_includedir}/ompt-multiplex.h
%{_libdir}/cmake/openmp

%if %{with fortran}
%files fortran-devel
%defattr(644,root,root,755)
%{_includedir}/omp_lib.h
%{_includedir}/omp_lib.mod
%{_includedir}/omp_lib_kinds.mod
%endif

%files gdb
%defattr(644,root,root,755)
%dir %{_datadir}/gdb/python/ompd
%{_datadir}/gdb/python/ompd/*.py
# FIXME: should be in arch-dependent directory
%attr(755,root,root) %{_datadir}/gdb/python/ompd/ompdModule.so
