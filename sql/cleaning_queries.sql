-- Table    : bilingual_3tier_dataset


-- Total row count
SELECT COUNT(*) AS total
FROM bilingual_3tier_dataset;


-- Turn count distribution to identify aberrant values
SELECT turns, COUNT(*) AS nb
FROM bilingual_3tier_dataset
GROUP BY turns
ORDER BY turns DESC;


-- Tier and language distribution before cleaning
SELECT
    label,
    language,
    COUNT(*) AS nb,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) AS pct
FROM bilingual_3tier_dataset
GROUP BY label, language
ORDER BY label, language;


-- Filter: keep conversations between 6 and 30 turns
CREATE TABLE bilingual_3tier_clean AS
SELECT *
FROM bilingual_3tier_dataset
WHERE turns BETWEEN 6 AND 30;


-- Rows removed
SELECT
    (SELECT COUNT(*) FROM bilingual_3tier_dataset) AS before_cleaning,
    (SELECT COUNT(*) FROM bilingual_3tier_clean)   AS after_cleaning,
    (SELECT COUNT(*) FROM bilingual_3tier_dataset)
        - (SELECT COUNT(*) FROM bilingual_3tier_clean) AS removed;


-- Tier and language distribution after cleaning
SELECT
    label,
    language,
    COUNT(*) AS nb,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) AS pct
FROM bilingual_3tier_clean
GROUP BY label, language
ORDER BY label, language;


-- Turn count stats after cleaning
SELECT
    MIN(turns)          AS min_turns,
    MAX(turns)          AS max_turns,
    ROUND(AVG(turns), 1) AS avg_turns
FROM bilingual_3tier_clean;


