%define		php_name	php%{?php_suffix}
%define		modname	sphinx
Summary:	%{modname} - client for sphinx SQL full-text search engine
Name:		%{php_name}-pecl-%{modname}
Version:	1.2.0
Release:	2
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	74e23a18f8cea31d64735f2cf5a3115c
URL:		http://pecl.php.net/package/sphinx/
BuildRequires:	libsphinxclient-devel
BuildRequires:	%{php_name}-devel >= 4:5.0.4
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Provides:	php(sphinx)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Client extension for Sphinx - Opensource SQL full-text search engine.

%prep
%setup -qc
mv %{modname}-%{version}/* .

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	EXTENSION_DIR=%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc CREDITS
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
