%define debug_package %{nil}
# define _unpackaged_files_terminate_build 0
# disable repacking jars
%define __os_install_post %{nil}
%global initd_dir %{_sysconfdir}/rc.d/init.d

Name:       hadoop
Version:    %{VERSION}
Release:    1%{?dist}
Summary:    Apache Spark is a multi-language engine for executing data engineering, data science, and machine learning on single-node machines or clusters.
Group:      Applications/Internet
License:    Apache 2.0
URL:        https://spark.apache.org/
Source0:    %{name}-%{version}.tgz
BuildRoot:  %{_tmppath}/apache-%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Packager:   Shuaipeng Lee <lishuaipeng651@gmail.com>

AutoReqProv: no

%description
Apache Spark is a multi-language engine for executing data engineering, data science, and machine learning on single-node machines or clusters.


%prep
%setup -q -n %{name}-%{version}

%build

%install
%{__rm} -rf %{buildroot}

%{__install} -d -m 0755 %{buildroot}
%{__install} -d -m 0755 %{buildroot}/usr/lib/%{name}

%{__cp} -rp ./* %{buildroot}/usr/lib/%{name}



%pre
if ! /usr/bin/id hdfs &>/dev/null; then
    /usr/sbin/useradd -r -d /var/lib/hdfs -s /bin/sh -c "hdfs" hdfs || \
        %logmsg "Unexpected error adding user \"hdfs\". Aborting installation."
    # /sbin/usermod -a -G hadoop spark
fi

%post
systemctl daemon-reload

%preun

%postun
systemctl daemon-reload
if [ $1 -eq 0 ]; then
    /usr/sbin/userdel hdfs || %logmsg "User \"hdfs\" could not be deleted."
fi

%clean
%{__rm} -rf %{buildroot}

%files 
%defattr(-,root,root,755)
/usr/lib/%{name}
