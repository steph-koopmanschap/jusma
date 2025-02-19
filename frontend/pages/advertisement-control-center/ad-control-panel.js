import { MobileDetectSSR } from "@/shared/model";

export default function adControlPanel() {
    //Redirect user to the dashboard if they are not logged in.
    useRequireAuth("/dashboard");

    return (
        <div>
            <h1 className="text-xl">Ad Control Panel</h1>
            <h2>Nothing here yet...</h2>
        </div>
    );
}

export const getServerSideProps = async (ctx) => {
    const { isMobile } = MobileDetectSSR(ctx);
    return {
        props: { isSSRMobile: isMobile }
    };
};
