%define _enable_debug_packages %{nil}
%define debug_package          %{nil}

%define build_diet 0

# commandline overrides:
# rpm -ba|--rebuild --with 'xxx'
%{?_with_diet: %{expand: %%define build_diet 1}}

Summary:	Check rootkits
Name:		chkrootkit
Version:	0.49
Release:	8
License:	BSD
Group:		Monitoring
Url:		http://www.chkrootkit.org/
Source0:	ftp://ftp.pangeia.com.br/pub/seg/pac/%{name}-%{version}.tar.bz2
Patch0:		chkrootkit_fix_apache_false_positive.diff
Patch1:		chkrootkit-0.49-bug57979.diff
%if %{build_diet}
BuildRequires:	dietlibc-devel >= 0.32
%endif
BuildRequires:	glibc-static-devel
Requires:	binutils
Requires:	coreutils
Requires:	findutils
Requires:	gawk
Requires:	grep
Requires:	net-tools
Requires:	procps
Requires:	sed

%description
Chkrootkit is a tool to locally check for signs of a rootkit.

%files
%doc ACKNOWLEDGMENTS README* COPYRIGHT
%{_sbindir}/*
%{_libdir}/%{name}

#----------------------------------------------------------------------------

%prep
%setup -q
%patch0 -p0
%patch1 -p0

# instead of a static patch
chmod 644 *
for i in `ls -1 *.c|sed "s/\.c//"`; do
    perl -pi -e "s|\./${i}|%{_libdir}/%{name}/${i}|g" %{name}
done

%build
%if %{build_diet}
# OE: use the power of dietlibc
make CC="diet gcc" CFLAGS="-DHAVE_LASTLOG_H -DLASTLOG_FILENAME='\"/var/log/lastlog\"' -DWTMP_FILENAME='\"/var/log/wtmp\"' -Os  -s -static" LDFLAGS=-static
%else
make CFLAGS="-DHAVE_LASTLOG_H -DLASTLOG_FILENAME='\"/var/log/lastlog\"' -DWTMP_FILENAME='\"/var/log/wtmp\"'" LDFLAGS=-static
%endif

%install
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_libdir}/%{name}

install chkrootkit %{buildroot}%{_sbindir}/
install check_wtmpx chkdirs chklastlog chkproc chkutmp chkwtmp ifpromisc strings-static %{buildroot}%{_libdir}/%{name}/


