# Vendored shared template — DO NOT EDIT

Byte-identical copies of the shared GEMS template tools, per protocol rule 2
("reuse, don't rebuild; no private forks"). Copied 2026-11-04 from
`karagemop466-tech/GEMSDOEkarage3` @ `6b0d7cd64b06c7b694eeae70032afc761f869171`,
whose `registry/shared_template_97597a.json` pins them to
`buffedlizard55-lab/GEMSDOE32` @ `97597a066d1c61d2c226fdba349716f41b30c1c6`
(that repo returns HTTP 404 on 2026-11-04, so upstream cannot be re-fetched;
hashes below were verified against the pin file at copy time).

| File | SHA-256 |
|---|---|
| scripts/evaluate_holdout.py | 21ed7f6460d876dc0eb83d8c01d3843ee660f43bb73576eb3f0adb1a07e61dbb |
| scripts/submission_writer.py | 663bc075d90cdfa8d440fa201eeb87fba2783c503562e06044a705963d76bcf6 |
| src/gems32/holdout.py | 9ce9cf359f4d7b7fa844dd8f208ec00c3e6c15afef5d724d9014320b944d318d |
| src/gems32/submission.py | d397118a7165f674ba45bdea89b65852f2a24450edaa9b7e00e7cd5b87f0b9e1 |
| src/gems32/metric.py | 382de3eb6d77d549e01bafa718fd01f5a7132263be0b6925dbd5a40a24025289 |
| src/gems32/paths.py | ceb7c79097958beff1f618e608491c3528341b14ee8b2e9cdcfafe1406230b69 |

Known upstream issues recorded by the sister repo (not silently fixed here):
GEMSDOE32 issues #37, #39, #41, #42, #51, #60–#63, #66 (repo currently 404).
The metric implementation was independently cross-checked in Korea7 against a
literal transcription of the official DrivenData equations
(`tests/test_metric_official.py`) and reproduces the sister repo's nine-site
holdout table to full printed precision.
