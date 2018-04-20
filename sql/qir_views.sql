-- view to see how often progress reports come with financial attachments
-- note: no with more of one case than the other exclude zero reports, so counts add up to total reports.
create or replace view progess_financial_report_cooccurence as
  with
      financial_reports as
    (select ins.case_number, count(rep.id) as no_financial_reports
     from company_insolvents ins
       join reports rep on rep.insolvent_id = ins.id
     where right(rep.identification, 1) = 'B'
     group by ins.case_number),
      progress_reports as (
      (select ins.case_number, count(rep.id) as no_progress_reports
       from company_insolvents ins
         join reports rep on rep.insolvent_id = ins.id
       where right(rep.identification, 1) != 'B'
       group by ins.case_number)
    ),
      report_counts as (
        select
          case when frep.case_number is not null then
            frep.case_number
          else prep.case_number end,
          no_progress_reports,
          no_financial_reports
        from financial_reports frep full outer join progress_reports prep
            on frep.case_number = prep.case_number
    )
  select (select count(*) from report_counts where no_financial_reports is null) as no_cases_with_zero_financial_reports,
         (select count(*) from report_counts where no_progress_reports is null) as no_cases_with_zero_progress_reports,
         (select count(*) from report_counts where no_progress_reports > no_financial_reports and no_financial_reports notnull) as no_cases_with_more_progress_reports,
         (select count(*) from report_counts where no_progress_reports < no_financial_reports and no_progress_reports notnull) as no_cases_with_more_financial_report,
         (select count(*) from report_counts where no_progress_reports = no_financial_reports) as no_cases_with_equal_no_of_both_reports;
