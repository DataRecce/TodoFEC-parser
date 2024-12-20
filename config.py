import polars as pl

RAW_DATA_DIR = "datarecce-todofec/raw"
PARQUERT_DIR = "datarecce-todofec/parquet"

S3_BUCKET_NAME = "cg-519a459a-0ea3-42c2-b7bc-fa1143481f74"
S3_REGION_NAME = "us-gov-west-1"
ELECTRONIC_FEC_PREFIX = "bulk-downloads/lectronic/"

SUMMARY_FILES = [
    {
        "category": "all_candidates",
        "year": 2024,
        "key": "bulk-downloads/2024/weball24.zip",
    },
    {
        "category": "all_candidates",
        "year": 2020,
        "key": "bulk-downloads/2020/weball20.zip",
    },
    {
        "category": "candidate_master",
        "year": 2024,
        "key": "bulk-downloads/2024/cn24.zip",
    },
    {
        "category": "candidate_committee_linkage",
        "year": 2024,
        "key": "bulk-downloads/2024/ccl24.zip",
    },
    {"category": "house_senate", "year": 2024, "key": "bulk-downloads/2024/webl24.zip"},
    {
        "category": "committee_master",
        "year": 2024,
        "key": "bulk-downloads/2024/cm24.zip",
    },
    {"category": "pac_summary", "year": 2024, "key": "bulk-downloads/2024/webk24.zip"},
    # Skip this one, the zip file too large (2.86 GB)
    # {
    #     "category": "contributions_by_individuals",
    #     "year": 2024,
    #     "key" :"bulk-downloads/2024/indiv24.zip",
    # },
    {
        "category": "contributions_from_committees_to_candidates",
        "year": 2024,
        "key": "bulk-downloads/2024/pas224.zip",
    },
    {
        "category": "contributions_from_committees_to_candidates",
        "year": 2020,
        "key": "bulk-downloads/2020/pas220.zip",
    },
    {
        "category": "transactions_between_committees",
        "year": 2024,
        "key": "bulk-downloads/2024/oth24.zip",
    },
    {
        "category": "operating_expenditures",
        "year": 2024,
        "key": "bulk-downloads/2024/oppexp24.zip",
    },
]

SCHEMAS = {
    "all_candidates": {
        "CAND_ID": pl.Utf8,
        "CAND_NAME": pl.Utf8,
        "CAND_ICI": pl.Utf8,
        "PTY_CD": pl.Utf8,
        "CAND_PTY_AFFILIATION": pl.Utf8,
        "TTL_RECEIPTS": pl.Decimal(14, 2),
        "TRANS_FROM_AUTH": pl.Decimal(14, 2),
        "TTL_DISB": pl.Decimal(14, 2),
        "TRANS_TO_AUTH": pl.Decimal(14, 2),
        "COH_BOP": pl.Decimal(14, 2),
        "COH_COP": pl.Decimal(14, 2),
        "CAND_CONTRIB": pl.Decimal(14, 2),
        "CAND_LOANS": pl.Decimal(14, 2),
        "OTHER_LOANS": pl.Decimal(14, 2),
        "CAND_LOAN_REPAY": pl.Decimal(14, 2),
        "OTHER_LOAN_REPAY": pl.Decimal(14, 2),
        "DEBTS_OWED_BY": pl.Decimal(14, 2),
        "TTL_INDIV_CONTRIB": pl.Decimal(14, 2),
        "CAND_OFFICE_ST": pl.Utf8,
        "CAND_OFFICE_DISTRICT": pl.Utf8,
        "SPEC_ELECTION": pl.Utf8,
        "PRIM_ELECTION": pl.Utf8,
        "RUN_ELECTION": pl.Utf8,
        "GEN_ELECTION": pl.Utf8,
        "GEN_ELECTION_PRECENT": pl.Decimal(7, 4),
        "OTHER_POL_CMTE_CONTRIB": pl.Decimal(14, 2),
        "POL_PTY_CONTRIB": pl.Decimal(14, 2),
        "CVG_END_DT": pl.Utf8,
        "INDIV_REFUNDS": pl.Decimal(14, 2),
        "CMTE_REFUNDS": pl.Decimal(14, 2),
    },
    "candidate_master": {
        "CAND_ID": pl.Utf8,
        "CAND_NAME": pl.Utf8,
        "CAND_PTY_AFFILIATION": pl.Utf8,
        "CAND_ELECTION_YR": pl.Utf8,
        "CAND_OFFICE_ST": pl.Utf8,
        "CAND_OFFICE": pl.Utf8,
        "CAND_OFFICE_DISTRICT": pl.Utf8,
        "CAND_ICI": pl.Utf8,
        "CAND_STATUS": pl.Utf8,
        "CAND_PCC": pl.Utf8,
        "CAND_ST1": pl.Utf8,
        "CAND_ST2": pl.Utf8,
        "CAND_CITY": pl.Utf8,
        "CAND_ST": pl.Utf8,
        "CAND_ZIP": pl.Utf8,
    },
    "candidate_committee_linkage": {
        "CAND_ID": pl.Utf8,
        "CAND_ELECTION_YR": pl.Utf8,
        "FEC_ELECTION_YR": pl.Utf8,
        "CMTE_ID": pl.Utf8,
        "CMTE_TP": pl.Utf8,
        "CMTE_DSGN": pl.Utf8,
        "LINKAGE_ID": pl.Utf8,
    },
    "house_senate": {
        "CAND_ID": pl.Utf8,
        "CAND_NAME": pl.Utf8,
        "CAND_ICI": pl.Utf8,
        "PTY_CD": pl.Utf8,
        "CAND_PTY_AFFILIATION": pl.Utf8,
        "TTL_RECEIPTS": pl.Decimal(14, 2),
        "TRANS_FROM_AUTH": pl.Decimal(14, 2),
        "TTL_DISB": pl.Decimal(14, 2),
        "TRANS_TO_AUTH": pl.Decimal(14, 2),
        "COH_BOP": pl.Decimal(14, 2),
        "COH_COP": pl.Decimal(14, 2),
        "CAND_CONTRIB": pl.Decimal(14, 2),
        "CAND_LOANS": pl.Decimal(14, 2),
        "OTHER_LOANS": pl.Decimal(14, 2),
        "CAND_LOAN_REPAY": pl.Decimal(14, 2),
        "OTHER_LOAN_REPAY": pl.Decimal(14, 2),
        "DEBTS_OWED_BY": pl.Decimal(14, 2),
        "TTL_INDIV_CONTRIB": pl.Decimal(14, 2),
        "CAND_OFFICE_ST": pl.Utf8,
        "CAND_OFFICE_DISTRICT": pl.Utf8,
        "SPEC_ELECTION": pl.Utf8,
        "PRIM_ELECTION": pl.Utf8,
        "RUN_ELECTION": pl.Utf8,
        "GEN_ELECTION": pl.Utf8,
        "GEN_ELECTION_PRECENT": pl.Decimal(7, 4),
        "OTHER_POL_CMTE_CONTRIB": pl.Decimal(14, 2),
        "POL_PTY_CONTRIB": pl.Decimal(14, 2),
        "CVG_END_DT": pl.Utf8,
        "INDIV_REFUNDS": pl.Decimal(14, 2),
        "CMTE_REFUNDS": pl.Decimal(14, 2),
    },
    "committee_master": {
        "CMTE_ID": pl.Utf8,
        "CMTE_NM": pl.Utf8,
        "TRES_NM": pl.Utf8,
        "CMTE_ST1": pl.Utf8,
        "CMTE_ST2": pl.Utf8,
        "CMTE_CITY": pl.Utf8,
        "CMTE_ST": pl.Utf8,
        "CMTE_ZIP": pl.Utf8,
        "CMTE_DSGN": pl.Utf8,
        "CMTE_TP": pl.Utf8,
        "CMTE_PTY_AFFILIATION": pl.Utf8,
        "CMTE_FILING_FREQ": pl.Utf8,
        "ORG_TP": pl.Utf8,
        "CONNECTED_ORG_NM": pl.Utf8,
        "CAND_ID": pl.Utf8,
    },
    "pac_summary": {
        "CMTE_ID": pl.Utf8,
        "CMTE_NM": pl.Utf8,
        "CMTE_TP": pl.Utf8,
        "CMTE_DSGN": pl.Utf8,
        "CMTE_FILING_FREQ": pl.Utf8,
        "TTL_RECEIPTS": pl.Decimal(14, 2),
        "TRANS_FROM_AFF": pl.Decimal(14, 2),
        "INDV_CONTRIB": pl.Decimal(14, 2),
        "OTHER_POL_CMTE_CONTRIB": pl.Decimal(14, 2),
        "CAND_CONTRIB": pl.Decimal(14, 2),
        "CAND_LOANS": pl.Decimal(14, 2),
        "TTL_LOANS_RECEIVED": pl.Decimal(14, 2),
        "TTL_DISB": pl.Decimal(14, 2),
        "TRANF_TO_AFF": pl.Decimal(14, 2),
        "INDV_REFUNDS": pl.Decimal(14, 2),
        "OTHER_POL_CMTE_REFUNDS": pl.Decimal(14, 2),
        "CAND_LOAN_REPAY": pl.Decimal(14, 2),
        "LOAN_REPAY": pl.Decimal(14, 2),
        "COH_BOP": pl.Decimal(14, 2),
        "COH_COP": pl.Decimal(14, 2),
        "DEBTS_OWED_BY": pl.Decimal(14, 2),
        "NONFED_TRANS_RECEIVED": pl.Decimal(14, 2),
        "CONTRIB_TO_OTHER_CMTE": pl.Decimal(14, 2),
        "IND_EXP": pl.Decimal(14, 2),
        "PTY_COORD_EXP": pl.Decimal(14, 2),
        "NONFED_SHARE_EXP": pl.Decimal(14, 2),
        "CVG_END_DT": pl.Utf8,
    },
    "contributions_by_individuals": {
        "CMTE_ID": pl.Utf8,
        "AMNDT_IND": pl.Utf8,
        "RPT_TP": pl.Utf8,
        "TRANSACTION_PGI": pl.Utf8,
        "IMAGE_NUM": pl.Utf8,  # Using Utf8 for both formats of image number
        "TRANSACTION_TP": pl.Utf8,
        "ENTITY_TP": pl.Utf8,
        "NAME": pl.Utf8,
        "CITY": pl.Utf8,
        "STATE": pl.Utf8,
        "ZIP_CODE": pl.Utf8,
        "EMPLOYER": pl.Utf8,
        "OCCUPATION": pl.Utf8,
        "TRANSACTION_DT": pl.Utf8,
        "TRANSACTION_AMT": pl.Decimal(14, 2),
        "OTHER_ID": pl.Utf8,
        "TRAN_ID": pl.Utf8,
        "FILE_NUM": pl.Utf8,
        "MEMO_CD": pl.Utf8,
        "MEMO_TEXT": pl.Utf8,
        "SUB_ID": pl.Utf8,
    },
    "contributions_from_committees_to_candidates": {
        "CMTE_ID": pl.Utf8,
        "AMNDT_IND": pl.Utf8,
        "RPT_TP": pl.Utf8,
        "TRANSACTION_PGI": pl.Utf8,
        "IMAGE_NUM": pl.Utf8,  # Using Utf8 for both formats of image number
        "TRANSACTION_TP": pl.Utf8,
        "ENTITY_TP": pl.Utf8,
        "NAME": pl.Utf8,
        "CITY": pl.Utf8,
        "STATE": pl.Utf8,
        "ZIP_CODE": pl.Utf8,
        "EMPLOYER": pl.Utf8,
        "OCCUPATION": pl.Utf8,
        "TRANSACTION_DT": pl.Utf8,
        "TRANSACTION_AMT": pl.Decimal(14, 2),
        "OTHER_ID": pl.Utf8,
        "CAND_ID": pl.Utf8,
        "TRAN_ID": pl.Utf8,
        "FILE_NUM": pl.Utf8,
        "MEMO_CD": pl.Utf8,
        "MEMO_TEXT": pl.Utf8,
        "SUB_ID": pl.Utf8,
    },
    "transactions_between_committees": {
        "CMTE_ID": pl.Utf8,
        "AMNDT_IND": pl.Utf8,
        "RPT_TP": pl.Utf8,
        "TRANSACTION_PGI": pl.Utf8,
        "IMAGE_NUM": pl.Utf8,
        "TRANSACTION_TP": pl.Utf8,
        "ENTITY_TP": pl.Utf8,
        "NAME": pl.Utf8,
        "CITY": pl.Utf8,
        "STATE": pl.Utf8,
        "ZIP_CODE": pl.Utf8,
        "EMPLOYER": pl.Utf8,
        "OCCUPATION": pl.Utf8,
        "TRANSACTION_DT": pl.Utf8,
        "TRANSACTION_AMT": pl.Decimal(14, 2),
        "OTHER_ID": pl.Utf8,
        "TRAN_ID": pl.Utf8,
        "FILE_NUM": pl.Utf8,
        "MEMO_CD": pl.Utf8,
        "MEMO_TEXT": pl.Utf8,
        "SUB_ID": pl.Utf8,
    },
    "operating_expenditures": {
        "CMTE_ID": pl.Utf8,
        "AMNDT_IND": pl.Utf8,
        "RPT_YR": pl.Utf8,
        "RPT_TP": pl.Utf8,
        "IMAGE_NUM": pl.Utf8,
        "LINE_NUM": pl.Utf8,
        "FORM_TP_CD": pl.Utf8,
        "SCHED_TP_CD": pl.Utf8,
        "NAME": pl.Utf8,
        "CITY": pl.Utf8,
        "STATE": pl.Utf8,
        "ZIP_CODE": pl.Utf8,
        "TRANSACTION_DT": pl.Utf8,
        "TRANSACTION_AMT": pl.Decimal(14, 2),
        "TRANSACTION_PGI": pl.Utf8,
        "PURPOSE": pl.Utf8,
        "CATEGORY": pl.Utf8,
        "CATEGORY_DESC": pl.Utf8,
        "MEMO_CD": pl.Utf8,
        "MEMO_TEXT": pl.Utf8,
        "ENTITY_TP": pl.Utf8,
        "SUB_ID": pl.Utf8,
        "FILE_NUM": pl.Utf8,
        "TRAN_ID": pl.Utf8,
        "BACK_REF_TRAN_ID": pl.Utf8,
    },
}
