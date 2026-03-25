# GitHub Repository Setup

This guide helps you set up this project as a GitHub repository.

## Prerequisites

- GitHub account
- Git installed locally
- SSH key configured (optional but recommended)

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Fill in repository name: `vm-manager`
3. Choose description:
   ```
   A powerful web-based GUI for managing virtual machines on Ubuntu servers. 
   Supports KVM, Xen, OpenVZ with one-click deployment, templates, monitoring & automation.
   ```
4. Choose visibility:
   - **Public** - For open-source community project
   - **Private** - For internal/commercial use

5. **Do NOT** initialize with:
   - README (we have one)
   - .gitignore (we have one)
   - License (we have MIT license)

6. Click **Create repository**

## Step 2: Push Local Repository

### Using HTTPS (Easier for beginners)

```bash
cd vm-manager

# Initialize git if not already done
git init

# Add all files
git add .

# Initial commit
git commit -m "Initial commit: VM Manager web interface"

# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/vm-manager.git

# Rename branch to main if needed
git branch -M main

# Push to GitHub
git push -u origin main
```

### Using SSH (Recommended)

```bash
cd vm-manager

# Initialize git if not already done
git init

# Add all files
git add .

# Initial commit
git commit -m "Initial commit: VM Manager web interface"

# Add remote repository with SSH
git remote add origin git@github.com:YOUR_USERNAME/vm-manager.git

# Rename branch to main if needed
git branch -M main

# Push to GitHub
git push -u origin main
```

## Step 3: Customize Repository

### Update README.md
Replace all instances of:
- `yourusername` → Your GitHub username
- `your-secret-key-change-in-production` → Generate a real secret key

Generate secret key:
```bash
# Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Using OpenSSL
openssl rand -base64 32
```

### Update CONTRIBUTING.md
- Add your contact email
- Update any community guidelines

### Update DEPLOYMENT.md
- Add your domain name
- Update support email

## Step 4: Configure GitHub Features

### 1. Add Repository Topics
Go to Repository Settings → General → Topics

Add:
- `vm-management`
- `kvm`
- `virtualization`
- `fastapi`
- `react`
- `docker`
- `libvirt`

### 2. Enable GitHub Pages (Optional)
For documentation hosting:
1. Go to Settings → Pages
2. Select Source: `Deploy from a branch`
3. Select Branch: `main` / `docs`
4. Save

### 3. Add Branch Protection
To require code reviews:
1. Go to Settings → Branches
2. Add rule for `main` branch
3. Enable:
   - Require pull request reviews
   - Require status checks
   - Include administrators

### 4. Set Up CI/CD
GitHub Actions workflow is already configured:
- File: `.github/workflows/ci.yml`
- Automatically runs tests on push/PR

## Step 5: Add Collaborators

1. Go to Settings → Collaborators
2. Click "Add people"
3. Search for GitHub usernames
4. Select permission level

## Step 6: Create Initial Issues

Use these templates to create issues:

### Issue 1: Documentation
```markdown
- [ ] Add web console (VNC/SPICE) support
- [ ] Create user tutorials
- [ ] Add architecture documentation
- [ ] Create API client libraries
```

### Issue 2: Features
```markdown
Priority features for v1.1:
- [ ] Two-factor authentication
- [ ] VM snapshots & cloning
- [ ] Prometheus monitoring integration
- [ ] Terraform provider
```

## Step 7: Documentation

### Create Wiki Pages (Optional)
1. Go to Repository → Wiki
2. Create pages:
   - Installation Guide
   - Architecture Overview
   - API Examples
   - Troubleshooting

### Create Discussions (Optional)
Enable Discussions for community engagement:
1. Go to Settings → General
2. Enable "Discussions"
3. Create discussion categories:
   - Announcements
   - General
   - Ideas
   - Q&A

## Step 8: Set Up Releases

Create first release:

```bash
# Tag the current version
git tag -a v1.0.0 -m "Initial release of VM Manager"

# Push tag to GitHub
git push origin v1.0.0
```

Then on GitHub:
1. Go to Releases
2. Click "Create a new release"
3. Select tag: `v1.0.0`
4. Add release notes
5. Add download links if applicable

## Step 9: Continuous Integration

The CI pipeline (.github/workflows/ci.yml) will:
- ✅ Run Python linting and tests
- ✅ Run JavaScript build and tests
- ✅ Build Docker images
- ✅ Check code quality

Verify it's working:
1. Make a small change
2. Create a pull request
3. Observe GitHub Actions running checks

## Step 10: Community Setup

### Add Code of Conduct
1. Create file: `.github/CODE_OF_CONDUCT.md`
2. Choose from template (e.g., Contributor Covenant)

### Add Security Policy
1. Create file: `SECURITY.md`
2. Add guidelines for reporting security issues

### Add Bug Report Template
Already included: `.github/ISSUE_TEMPLATE/bug_report.yml`

## Useful GitHub URLs

| What | URL |
|------|-----|
| Repository | `https://github.com/YOUR_USERNAME/vm-manager` |
| Issues | `https://github.com/YOUR_USERNAME/vm-manager/issues` |
| Pull Requests | `https://github.com/YOUR_USERNAME/vm-manager/pulls` |
| Releases | `https://github.com/YOUR_USERNAME/vm-manager/releases` |
| Wiki | `https://github.com/YOUR_USERNAME/vm-manager/wiki` |
| Discussions | `https://github.com/YOUR_USERNAME/vm-manager/discussions` |
| Actions | `https://github.com/YOUR_USERNAME/vm-manager/actions` |

## Update Local Configuration

### User info
```bash
git config user.name "Your Name"
git config user.email "your.email@example.com"

# For global config
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Set upstream
```bash
git remote set-url origin https://github.com/YOUR_USERNAME/vm-manager.git
```

## Making Changes

### Standard workflow
```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes
# ... edit files ...

# Stage and commit
git add .
git commit -m "Add: description of changes"

# Push to GitHub
git push origin feature/your-feature-name

# Create Pull Request on GitHub UI
```

## Additional Resources

- [GitHub Docs](https://docs.github.com)
- [Git Documentation](https://git-scm.com/doc)
- [GitHub Actions](https://github.com/features/actions)
- [Project Management](https://docs.github.com/en/issues)

## Support

- **GitHub Help**: https://support.github.com
- **Community**: https://github.community
- **Documentation**: https://docs.github.com

---

**Next Steps:**
1. ✅ Set up repository on GitHub
2. ✅ Push code to main branch
3. ✅ Follow QUICKSTART.md for development
4. ✅ Check Contributing.md to welcome contributors

Happy coding! 🚀
