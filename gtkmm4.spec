#
# Conditional build:
%bcond_without	static_libs	# static library

%define		atkmm_ver	2.29.1
%define		cairomm_ver	1.15.4
%define		glibmm_ver	2.68.0
%define		gtk4_ver	4.0.0
%define		pangomm_ver	2.48.0
Summary:	A C++ interface for the GTK+ (a GUI library for X)
Summary(pl.UTF-8):	Wrapper C++ dla GTK+
Name:		gtkmm4
Version:	4.0.1
Release:	1
License:	LGPL v2+
Group:		X11/Libraries
Source0:	https://download.gnome.org/sources/gtkmm/4.0/gtkmm-%{version}.tar.xz
# Source0-md5:	69774cc079b34dd006b7bc49d81fe324
URL:		https://www.gtkmm.org/
BuildRequires:	atkmm2.36-devel >= %{atkmm_ver}
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.11
BuildRequires:	cairomm1.16-devel >= %{cairomm_ver}
BuildRequires:	doxygen >= 1:1.8.9
BuildRequires:	gdk-pixbuf2-devel >= 2.36.0
BuildRequires:	glibmm2.68-devel >= %{glibmm_ver}
BuildRequires:	gtk4-devel >= %{gtk4_ver}
BuildRequires:	libepoxy-devel >= 1.2
BuildRequires:	libsigc++3-devel >= 3.0
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	libtool >= 2:2.0
BuildRequires:	mm-common >= 0.9.12
BuildRequires:	pangomm2.48-devel >= %{pangomm_ver}
BuildRequires:	perl-base >= 1:5.6.0
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.752
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	atkmm2.36 >= %{atkmm_ver}
Requires:	cairomm1.16 >= %{cairomm_ver}
Requires:	gdk-pixbuf2 >= 2.36.0
Requires:	glibmm2.68 >= %{glibmm_ver}
Requires:	gtk4 >= %{gtk4_ver}
Requires:	pangomm2.48 >= %{pangomm_ver}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package provides a C++ interface for GTK+ (the Gimp ToolKit) GUI
library. The interface provides a convenient interface for C++
programmers to create GUIs with GTK+'s flexible object-oriented
framework. Features include type safe callbacks, widgets that are
extensible using inheritance and over 110 classes that can be freely
combined to quickly create complex user interfaces.

%description -l pl.UTF-8
gtkmm jest wrapperem C++ dla Gimp ToolKit (GTK). GTK+ jest biblioteką
służącą do tworzenia graficznych interfejsów. W pakiecie znajduje się
także biblioteka gdkmm - wrapper C++ dla GDK (General Drawing Kit).

%package devel
Summary:	gtkmm and gdkmm header files
Summary(pl.UTF-8):	Pliki nagłówkowe gtkmm i gdkmm
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	atkmm2.36-devel >= %{atkmm_ver}
Requires:	cairomm1.16-devel >= %{cairomm_ver}
Requires:	gdk-pixbuf2-devel >= 2.36.0
Requires:	glibmm2.68-devel >= %{glibmm_ver}
Requires:	gtk4-devel >= %{gtk4_ver}
Requires:	libstdc++-devel >= 6:7
Requires:	pangomm2.48-devel >= %{pangomm_ver}

%description devel
Header files for gtkmm library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki gtkmm.

%package static
Summary:	gtkmm and gdkmm static libraries
Summary(pl.UTF-8):	Biblioteki statyczne gtkmm i gdkmm
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
gtkmm and gdkmm static libraries.

%description static -l pl.UTF-8
Biblioteki statyczne gtkmm i gdkmm.

%package apidocs
Summary:	Reference documentation for gtkmm and gdkmm
Summary(pl.UTF-8):	Szczegółowa dokumentacja gtkmm i gdkmm
Group:		Documentation
Requires:	devhelp
%{?noarchpackage}

%description apidocs
Reference documentation for gtkmm and gdkmm.

%description apidocs -l pl.UTF-8
Szczegółowa dokumentacja gtkmm i gdkmm.

%prep
%setup -q -n gtkmm-%{version}

# missing in release tarball, not needed for Linux
mkdir win32_installer
touch win32_installer/filelist.am \
	win32_installer/gtkmm-installer.nsi.in

%build
mm-common-prepare --copy --force
%{__libtoolize}
%{__aclocal} -I build
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-maintainer-mode \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_libdir}/libgtkmm-4.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgtkmm-4.0.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgtkmm-4.0.so
%{_libdir}/gtkmm-4.0
%{_includedir}/gtkmm-4.0
%{_pkgconfigdir}/gtkmm-4.0.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgtkmm-4.0.a
%endif

%files apidocs
%defattr(644,root,root,755)
%{_docdir}/gtkmm-4.0
%{_datadir}/devhelp/books/gtkmm-4.0
