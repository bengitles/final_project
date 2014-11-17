Structure of our folder

Docs/ directory
---------------------------
    README.md: this README file!
    final_project_flow_diagram.pdf: our flow diagrams
    screenshot1.png: screenshot of candidate layout
    screenshot2.png: screenshot of candidate layout + voting question
    screenshot3.png: golden question


Data/ directory
--------------------------
    ANES-2008-survey-questions.txt: CCB's dataset of questions 
    Batch_951674_batch_results.csv: one batch's answers to these questions
    Batch_951674_mock_clustered_candidates.csv: mock Crowdflower clustering after initial aggregation
    Other batch files: not used currently but may be used in the future


Src/ directory
--------------------------
    module/ : contains both aggregaation and QC modules
      --> aggregate_answers.py: CCB's dataset --> k means clustering over candidate preferences
      --> get_best_candidates.py: Crowdflower answers ---> find winning candidate
      --> data/: replication of data directory in root for testing purposes


