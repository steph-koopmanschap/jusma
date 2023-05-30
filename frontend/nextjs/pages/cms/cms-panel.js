import { useCheckAuthClientSide } from "@/features/auth/admin/index.js";
import ReportPanel from "@/widgets/report";

/*
    This is a page for moderators to review flagged / reported content on JASMA
    And to delete the content if needed or delete the report if the report was false.
*/

export default function CMS_Panel() {
    useCheckAuthClientSide("/cms/cms-login");

    return (
        <div>
            <ReportPanel />
        </div>
    );
}
