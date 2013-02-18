# OE: conditional switches
#(ie. use with rpm --rebuild):
#	--with diet	Compile chkrootkit against dietlibc
%define _enable_debug_packages %{nil}
%define debug_package          %{nil}

%define build_diet 0

# commandline overrides:
# rpm -ba|--rebuild --with 'xxx'
%{?_with_diet: %{expand: %%define build_diet 1}}

Summary:	Check rootkits
Name:		chkrootkit
Version:	0.49
Release:	6
Source0:	ftp://ftp.pangeia.com.br/pub/seg/pac/%{name}-%{version}.tar.bz2
Patch0:     chkrootkit_fix_apache_false_positive.diff
Patch1:		chkrootkit-0.49-bug57979.diff
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


%changelog
* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 0.49-5mdv2011.0
+ Revision: 610136
- rebuild

* Thu Mar 11 2010 Oden Eriksson <oeriksson@mandriva.com> 0.49-4mdv2010.1
+ Revision: 518002
- fix #57979 (chkrootkit causes lots of traffic on NFS share)

* Mon Jan 18 2010 Michael Scherer <misc@mandriva.org> 0.49-3mdv2010.1
+ Revision: 493355
- fix chkrootkit giving false positive when apache is running,
  as the buffer is too small for a long process line.

* Fri Sep 11 2009 Michael Scherer <misc@mandriva.org> 0.49-2mdv2010.1
+ Revision: 438091
- disable dietlibc, to prevent bug #50727, due to incomplete dietlibc getpriority
  support.

* Sun Aug 09 2009 Frederik Himpe <fhimpe@mandriva.org> 0.49-1mdv2010.0
+ Revision: 412556
- update to new version 0.49

* Thu Aug 07 2008 Thierry Vignaud <tv@mandriva.org> 0.48-3mdv2009.0
+ Revision: 266507
- rebuild early 2009.0 package (before pixel changes)

* Tue Jun 10 2008 Oden Eriksson <oeriksson@mandriva.com> 0.48-2mdv2009.0
+ Revision: 217536
- rebuilt against dietlibc-devel-0.32

* Tue Jan 08 2008 Emmanuel Andry <eandry@mandriva.org> 0.48-1mdv2008.1
+ Revision: 146744
- New version
- drop patch

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Thu Aug 23 2007 Thierry Vignaud <tv@mandriva.org> 0.47-4mdv2008.0
+ Revision: 69706
- fileutils, sh-utils & textutils have been obsoleted by coreutils a long time ago

* Fri Aug 10 2007 Olivier Blin <oblin@mandriva.com> 0.47-3mdv2008.0
+ Revision: 61483
- really fix wtmp file location

* Fri Aug 10 2007 Olivier Blin <oblin@mandriva.com> 0.47-2mdv2008.0
+ Revision: 61421
- install chkdirs
- fix check of chkproc in lkm test


* Fri Nov 17 2006 Emmanuel Andry <eandry@mandriva.org> 0.47-1mdv2007.0
+ Revision: 85403
- New version 0.47
- Import chkrootkit

