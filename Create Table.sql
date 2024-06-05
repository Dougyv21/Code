CREATE TABLE [dbo].[Industry] (
    [IndustryID]         INT              IDENTITY (1, 1) NOT FOR REPLICATION NOT NULL,
    [IndustryName]       VARCHAR (50)     NOT NULL,
    [Description]        VARCHAR (255)    NULL,
    [SICMin]             VARCHAR (4)      NULL,
    [SICMax]             VARCHAR (4)      NULL,
    [RecordStatusID]     TINYINT          NOT NULL,
    [DateModified]       DATETIME         NULL,
    [audit_row_id]       UNIQUEIDENTIFIER ROWGUIDCOL NOT NULL,
    [DefaultAddMeStatus] BIT              NOT NULL,
    [ReplaceIndustryID]  INT              NULL,
    CONSTRAINT [PK_Industry] PRIMARY KEY CLUSTERED ([IndustryID] ASC) WITH (FILLFACTOR = 90)
);

CREATE TABLE [dbo].[Engagement](
    [EngagementID] [int] IDENTITY(1,1) NOT FOR REPLICATION NOT NULL,
    [EngagementName] [varchar](256) NOT NULL,
    [FiscalYearEnd] [smalldatetime] NULL,
    [QuarterID] [smallint] NULL,
    [IPMFolder] [int] NULL,
    [EngagementTypeID] [int] NOT NULL,
    [NumberOfEntities] [int] NOT NULL,
    [DateAuditorOpinion] [datetime] NULL,
    [ReportIssueDate] [datetime] NULL,
    [ClientNumber] [int] NOT NULL,
    [ClientEIN] [char](9) NULL,
    [IndustryID] [int] NOT NULL,
    [SECID] [tinyint] NULL,
    [AcceleratedFilerID] [tinyint] NULL,
    [IsSECEngagement] [bit] NOT NULL,
    [Creator] [varchar](30) NOT NULL,
    [CreationDate] [datetime] NOT NULL,
    [IsCompleted] [bit] NOT NULL,
    [CompleteDate] [datetime] NULL,
    [RollForwardDate] [datetime] NULL,
    [DateModified] [datetime] NULL,
    [DocumentCount] [int] NOT NULL,
    [CaseWareFileDirectory] [varchar](512) NULL,
    [CaseWareFileName] [varchar](50) NULL,
    [IsDeprovisioned] [bit] NOT NULL,
    [IsSensitive] [bit] NOT NULL,
    [EngagementStatusID] [tinyint] NOT NULL,
    [ParentEngagementID] [int] NULL,
    [TaxFormID] [tinyint] NOT NULL,
    [RecordStatusID] [tinyint] NOT NULL,
    [ClientWebSiteAddress] [varchar](100) NULL,
    [LegalStatusID] [tinyint] NULL,
    [audit_row_id] [uniqueidentifier] ROWGUIDCOL  NOT NULL,
    [ArchiveStatus] [bit] NULL,
    [ClearSurveyNumber] [nvarchar](256) NULL,
    [ClearEngagementRowReferenceId] [int] NULL,
    [ClientBN] [char](9) NULL,
    [FactoryServiceVersionID] [int] NOT NULL,
    [MaterialChangeRequestId] [nvarchar](256) NULL,
CONSTRAINT [PK_Engagement] PRIMARY KEY CLUSTERED 
(
    [EngagementID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO;

CREATE TABLE [dbo].[Employee](
    [EmployeeId] NVARCHAR(10) NOT NULL,
    [DateEnd] DATETIME NULL,
    [LastName] NVARCHAR(50) NOT NULL,
    [FirstName] NVARCHAR(50) NOT NULL,
    [SubFunctionCode] INT NULL,
    [SubFunctionDescription] NVARCHAR(50) NULL,
    [LineOfBusinessId] NVARCHAR(10) NULL,
    [LocationCountry] NVARCHAR(10) NULL,
    CONSTRAINT [PK_Employee] PRIMARY KEY ([EmployeeId])
);