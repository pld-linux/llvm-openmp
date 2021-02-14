# TODO: offload library? (requires Intel COI Runtime + Intel MYO Runtime)
#
# Conditional build:
%bcond_without	fortran		# Fortran modules
#
Summary:	Intel OpenMP runtime library implementation for use with Clang
Summary(pl.UTF-8):	Implementacja biblioteki uruchomieniowej OpenMP firmy Intel dla kompilatora Clang
Name:		llvm-openmp
Version:	11.0.1
Release:	1
License:	BSD-like or MIT (OMP), Apache v2.0 (Archer)
Group:		Libraries
#Source0Download: https://github.com/llvm/llvm-project/releases/
Source0:	https://github.com/llvm/llvm-project/releases/download/llvmorg-%{version}/openmp-%{version}.src.tar.xz
# Source0-md5:	b92f907b7bf1fda41e792ce80983d5fa
URL:		https://openmp.llvm.org/
BuildRequires:	cmake >= 2.8
%{?with_fortran:BuildRequires:	gcc-fortran}
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

%prep
%setup -q -n openmp-%{version}.src

%build
install -d build
cd build
libsubdir=%{_lib}
%cmake .. \
%ifarch %{arm} ppc64
	-DLIBOMP_ARCH=%{iomp_arch} \
%endif
	-DLIBOMP_LIBDIR_SUFFIX="${libsuffix#lib}" \
	%{?with_fortran:-DLIBOMP_FORTRAN_MODULES=ON}

%{__make}

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
%doc CREDITS.txt LICENSE.txt www/{README.txt,Reference.pdf,*.{html,css}}
%attr(755,root,root) %{_libdir}/libarcher.so
%attr(755,root,root) %{_libdir}/libomp.so
%attr(755,root,root) %{_libdir}/libomptarget.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libiomp5.so
%{_libdir}/libarcher_static.a
%{_includedir}/omp.h
%{_includedir}/omp-tools.h
%{_includedir}/ompt.h
%{_includedir}/ompt-multiplex.h

%if %{with fortran}
%files fortran-devel
%defattr(644,root,root,755)
%{_includedir}/omp_lib.h
%{_includedir}/omp_lib.mod
%{_includedir}/omp_lib_kinds.mod
%endif
