# Maintainer's Guide

This guide is for maintainers of the AI Markdown Journal project.

## Architecture Principles

### Separation of Concerns

**`_core/` - System Files**
- Maintained by the project
- Can be updated via git pull
- Should remain generic and reusable
- No user-specific content

**`journal/` - User Content**
- Belongs to the user
- Never touched by updates
- Completely flexible
- Gitignored by default

### Versioning

Follow [Semantic Versioning](https://semver.org/):
- **Major (X.0.0)** - Breaking changes to structure or workflow
- **Minor (0.X.0)** - New features, templates, or guides
- **Patch (0.0.X)** - Bug fixes, doc improvements, minor updates

Update both:
1. `_core/VERSION`
2. `_core/CHANGELOG.md`

## Adding New Features

### New Template

```bash
# 1. Create template
touch _core/templates/new-template.md

# 2. Write guide
touch _core/docs/guides/new-template.md

# 3. Update CHANGELOG
# Add to [Unreleased] section

# 4. Increment version
echo "1.1.0" > _core/VERSION
```

### New Documentation

```bash
# Add to _core/docs/ or _core/docs/guides/
# Update README.md if it's a major feature
# Update CHANGELOG.md
```

### New Integration Example

```bash
# Create integration guide
touch _core/docs/integrations/tool-name.md

# Add example config to .ai-journal-config.json.example
# Update CHANGELOG.md
```

## Release Process

### 1. Update Version

```bash
# Update version number
echo "1.1.0" > _core/VERSION

# Update CHANGELOG
# Move [Unreleased] items to [1.1.0] with date
```

### 2. Test Changes

```bash
# Test setup script
./setup.sh

# Test update script
./update-core.sh

# Verify journal/ is protected
```

### 3. Commit and Tag

```bash
git add .
git commit -m "Release v1.1.0: [brief description]"
git tag v1.1.0
git push origin main --tags
```

### 4. Create GitHub Release

1. Go to Releases page
2. Click "Draft a new release"
3. Select the tag
4. Copy CHANGELOG entry as description
5. Publish release

## Testing

### Test Setup Script

```bash
# Create test directory
mkdir test-install
cd test-install

# Clone repo
git clone https://github.com/troylar/ai-journal-kit.git
cd ai-markdown-journal

# Run setup
./setup.sh

# Verify:
# - journal/ folder created
# - Example note copied
# - Config created
# - README in journal/
```

### Test Update Script

```bash
# Make some changes to _core/
# Commit them

# Run update
./update-core.sh

# Verify:
# - _core/ updated
# - journal/ untouched
# - Backup created
```

## File Organization Rules

### What Goes in `_core/`

**`_core/templates/`**
- Generic, reusable templates
- No user-specific content
- Include helpful comments and examples

**`_core/docs/`**
- Setup guides
- How-to documentation
- Best practices

**`_core/docs/guides/`**
- Detailed guides for each journal type
- Workflow explanations
- Tips and strategies

**`_core/instructions/`**
- AI coach system instructions
- Different instruction sets for different use cases
- Demo-safe versions

**`_core/examples/`**
- Filled-out example notes
- Should use generic content
- Demonstrate best practices

**`_core/scripts/`**
- Automation scripts
- Setup and update tools
- Maintenance utilities

### What NEVER Goes in `_core/`

- User journal entries
- Personal information
- Sensitive content
- User-specific customizations

### What Goes in `journal/`

- Nothing by default (user creates content)
- `.gitkeep` files to preserve structure
- README.md explaining the folder

## Common Maintenance Tasks

### Adding a New Template Type

1. Create template file: `_core/templates/type-template.md`
2. Write guide: `_core/docs/guides/type.md`
3. Add example: `_core/examples/type-example.md`
4. Update main README if major feature
5. Update CHANGELOG
6. Increment version

### Improving Existing Template

1. Edit template in `_core/templates/`
2. Update related guide if structure changed
3. Note in CHANGELOG under [Unreleased]
4. Increment patch version when releasing

### Fixing Documentation

1. Edit files in `_core/docs/`
2. Note in CHANGELOG (minor fixes can be batched)
3. Increment patch version

### Adding Integration Example

1. Create guide: `_core/docs/integrations/tool.md`
2. Add config example to `.ai-journal-config.json.example`
3. Update main README in "Integration Examples" section
4. Update CHANGELOG
5. Increment minor version

## Code of Conduct

### Reviewing Contributions

- Be welcoming and encouraging
- Provide constructive feedback
- Focus on the work, not the person
- Assume good intentions

### Accepting Pull Requests

Check:
- [ ] Changes are in `_core/` only (never `journal/`)
- [ ] Templates are generic and reusable
- [ ] Documentation is clear and helpful
- [ ] CHANGELOG is updated
- [ ] Version is incremented if needed
- [ ] Tests pass (setup/update scripts work)

### Community Engagement

- Respond to issues within 48 hours
- Help users troubleshoot
- Encourage customization and sharing
- Build inclusive community

## Security

### Sensitive Information

- Never commit API keys or tokens
- Keep `.ai-journal-config.json` in .gitignore
- Remind users to use private repos if version controlling journal/
- Review PRs for accidental sensitive data

### Dependencies

- Minimize external dependencies
- Keep to standard shell scripts and markdown
- Document any required tools
- Test across platforms (macOS, Linux, Windows/WSL)

## Support Channels

- **Issues** - Bug reports, feature requests
- **Discussions** - Questions, ideas, community
- **Pull Requests** - Code contributions
- **Discord/Slack** - Real-time community (if created)

## Resources

- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [Contributing Guidelines](../CONTRIBUTING.md)
- [Project README](../README.md)

---

**Thank you for maintaining this project and supporting the community!** 🙏

