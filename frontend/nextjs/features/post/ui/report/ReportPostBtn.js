import { ReportModal } from "./ReportModal";
import { useState } from "react";
import { useToast } from "@/shared/model";
import { handleReportPost } from "../../model/actions";

export const ReportPostBtn = ({ post_id }) => {
    const { notifyToast } = useToast();

    const [reportModalState, setReportModalState] = useState(false);
    const openReportModal = () => {
        setReportModalState(true);
    };
    const closeReportModal = () => {
        setReportModalState(false);
    };

    const handleSubmit = async () => {
        const report_reason = document.getElementById("reportReasonInput").value;
        console.log("report_reason", report_reason);

        const res = await handleReportPost(post_id, report_reason);
        if (res.success) {
            notifyToast("Report sent!");
            closeReportModal();
        } else {
            notifyToast(res.message);
        }
    };

    return (
        <>
            <button
                className="formButtonDefault outline-white border my-1"
                onClick={openReportModal}
            >
                Report
            </button>
            <ReportModal
                isOpen={reportModalState}
                onClose={closeReportModal}
                onSubmitModal={handleSubmit}
            />
        </>
    );
};
