# Changelog
All notable changes to this project will be documented in this file. See [conventional commits](https://www.conventionalcommits.org/) for commit guidelines.

- - -
## [v0.6.2](https://github.com/dcog989/dicmerge/compare/bcd6c25f548899076f77a8e2f8b1c02f2785a229..v0.6.2) - 2026-09-01
#### Continuous Integration
- pin setup-uv to v10.0.0 immutable tag - ([bcd6c25](https://github.com/dcog989/dicmerge/commit/bcd6c25f548899076f77a8e2f8b1c02f2785a229)) - dcog989

- - -

## [v0.6.1](https://github.com/dcog989/dicmerge/compare/eaa744adca8843bf22c212f972a84186469ac41a..v0.6.1) - 2026-09-01
#### Bug Fixes
- push correct tag ref in cog post-bump hooks - ([eaa744a](https://github.com/dcog989/dicmerge/commit/eaa744adca8843bf22c212f972a84186469ac41a)) - dcog989
#### Build system
- regenerate uv.lock in cog pre-bump hooks - ([624eadb](https://github.com/dcog989/dicmerge/commit/624eadbc85b7597a3944f18106db798cb514f3ca)) - dcog989

- - -

## [v0.6.0](https://github.com/dcog989/dicmerge/compare/c078cbce5fb91e3494273bfbfe9060313576650e..v0.6.0) - 2026-09-01
#### Build system
- push commits and tag after cog bump - ([c078cbc](https://github.com/dcog989/dicmerge/commit/c078cbce5fb91e3494273bfbfe9060313576650e)) - dcog989
#### Miscellaneous Chores
- update - ([df55411](https://github.com/dcog989/dicmerge/commit/df5541137caf065cea369c5f59caa69f39a0b9ea)) - dcog989

- - -

## [v0.5.1](https://github.com/dcog989/dicmerge/compare/e2835378adaee1a29fef1726995af29f7b372e40..v0.5.1) - 2026-09-01
#### Bug Fixes
- wrap backup creation in write-back error handling - ([b48a66e](https://github.com/dcog989/dicmerge/commit/b48a66ed70fea89139163d483356393bd93cd7c1)) - dcog989
- clarify output line under dry-run - ([4be38ba](https://github.com/dcog989/dicmerge/commit/4be38ba1f46041645fa1bae92210907bb3a12cd0)) - dcog989
- show write-back targets in dry-run - ([f0d042b](https://github.com/dcog989/dicmerge/commit/f0d042b8c5c755e6491850286eb856a7399db3ea)) - dcog989
- make --write-back flag work regardless of config - ([994b420](https://github.com/dcog989/dicmerge/commit/994b420cc1dfc18299a16e56458f93e70a835fc4)) - dcog989
- exclude Firefox crashrecovery backup dirs from discovery - ([4543124](https://github.com/dcog989/dicmerge/commit/4543124adfa48e7af30c28a1d6ad9a183d75f12d)) - dcog989
- stop dropping digit first line in plaintext scanner - ([f2da662](https://github.com/dcog989/dicmerge/commit/f2da6624a6a13f07f208c9dc74071449d90a381d)) - dcog989
- honor output encoding from config - ([f6980ba](https://github.com/dcog989/dicmerge/commit/f6980baa9f1c4933e38ff6b342a8f371579aecf8)) - dcog989
- refresh write-back backup on every run - ([9953ccf](https://github.com/dcog989/dicmerge/commit/9953ccf8f13f56dae1547d3684c7d3b3c8c4a6fb)) - dcog989
- honor write_back.enabled config and dry-run for write-back - ([b961b78](https://github.com/dcog989/dicmerge/commit/b961b781323d482576b64dec1b008da0f4afc2b7)) - dcog989
#### Documentation
- fix usage instructions - ([c62b76d](https://github.com/dcog989/dicmerge/commit/c62b76d20f1cc4dd3c6ac7981c69990d67de8876)) - dcog989
- readme ruff format - ([d2b5a5a](https://github.com/dcog989/dicmerge/commit/d2b5a5a35ec7ca15bf1e4c819e14c394d877634f)) - dcog989
- document write_back.enabled config toggle - ([e944839](https://github.com/dcog989/dicmerge/commit/e944839423cfd6d12c79b3cb85a76d1dfc3774ad)) - dcog989
- correct write-back behavior and document cocogitto + CI stack - ([c165d40](https://github.com/dcog989/dicmerge/commit/c165d400d53ee4c9ad446654cf62040d56ff03dd)) - dcog989
#### Build system
- migrate version bumping from version-bump script to cocogitto - ([e283537](https://github.com/dcog989/dicmerge/commit/e2835378adaee1a29fef1726995af29f7b372e40)) - dcog989
#### Continuous Integration
- add CI pipeline with lint, typecheck, and coverage gates - ([623ebec](https://github.com/dcog989/dicmerge/commit/623ebecd423a5cbce514090a15106fd80f0615e1)) - dcog989
#### Refactoring
- route --list-sources through core orchestration - ([433f93f](https://github.com/dcog989/dicmerge/commit/433f93f81178d60dff470cb44d4d00db98296af5)) - dcog989
- separate source discovery from config handling - ([26e8f65](https://github.com/dcog989/dicmerge/commit/26e8f65498e3ac1b4127648c74a01c9cbc8fc068)) - dcog989
- depend on Scanner abstraction in write-back - ([12aebd1](https://github.com/dcog989/dicmerge/commit/12aebd11900c8b7839c86f78f71c94d210cd9f86)) - dcog989
- close scanner dispatch via registry and matches() - ([9d984ce](https://github.com/dcog989/dicmerge/commit/9d984ce6b6e4beec3f5260dc6b08dfab7b0347ee)) - dcog989
- split run() into focused single-responsibility helpers - ([1d6342b](https://github.com/dcog989/dicmerge/commit/1d6342b5afa99a9ffe82284a7d8d493739cf184b)) - dcog989
- drop speculative multi-format output files - ([96f3163](https://github.com/dcog989/dicmerge/commit/96f3163ea02df63de4f456189bb68655ce443e18)) - dcog989
- remove unused missing_words helper - ([8f68879](https://github.com/dcog989/dicmerge/commit/8f68879485bddd4f55c47d737e3812e85ab48862)) - dcog989
- dedupe source discovery globbing in config - ([6b0ce2c](https://github.com/dcog989/dicmerge/commit/6b0ce2cb14393304608b5d87a94c51978eec8146)) - dcog989
- extract shared .rws skip check in core - ([9e2af66](https://github.com/dcog989/dicmerge/commit/9e2af66a27cdf504de78d7cedd8567f265013ac3)) - dcog989
- collapse duplicate scanner line-reading into base - ([bc2abe1](https://github.com/dcog989/dicmerge/commit/bc2abe1cd2537ec60908b7a561c9728cda53e022)) - dcog989

- - -

Changelog generated by [cocogitto](https://github.com/cocogitto/cocogitto).