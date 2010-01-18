# OE: conditional switches
#(ie. use with rpm --rebuild):
#	--with diet	Compile chkrootkit against dietlibc

%define build_diet 0

# commandline overrides:
# rpm -ba|--rebuild --with 'xxx'
%{?_with_diet: %{expand: %%define build_diet 1}}

Summary:	Check rootkits
Name:		chkrootkit
Version:	0.49
Release:	%mkrel 3
Source0:	ftp://ftp.pangeia.com.br/pub/seg/pac/%{name}-%{version}.tar.bz2
Patch0:     chkrootkit_fix_apache_false_positive.diff
URL:		http://www.chkrootkit.org/
License:	BSD
Group:		Monitoring
Requires:	binutils, coreutils, findutils, gawk, grep, net-tools, procps, sed
BuildRequires:  glibc-static-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%if %{build_diet}
BuildRequires:	dietlibc-devel >= 0.32
%endif

%description
Chkrootkit is a tool to locally check for signs of a rootkit.

%prep

%setup -q
%patch0 -p0

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
rm -rf %{buildroot}

install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_libdir}/%{name}

install chkrootkit %{buildroot}%{_sbindir}/
install check_wtmpx chkdirs chklastlog chkproc chkutmp chkwtmp ifpromisc strings-static %{buildroot}%{_libdir}/%{name}/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc ACKNOWLEDGMENTS README* COPYRIGHT
%{_sbindir}/*
%{_libdir}/%{name}
