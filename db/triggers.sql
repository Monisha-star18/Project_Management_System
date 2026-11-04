CREATE OR REPLACE FUNCTION public.auto_allot_project_lead()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN

    INSERT INTO public.project_allotments (
        project_id,
        employee_id
    )
    VALUES (
        NEW.project_id,
        NEW.lead_id
    );

    RETURN NEW;

END;
$$;


CREATE TRIGGER trg_auto_allot_project_lead
AFTER INSERT ON public.projects
FOR EACH ROW
EXECUTE FUNCTION public.auto_allot_project_lead();