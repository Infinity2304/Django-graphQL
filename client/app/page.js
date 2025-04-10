import Image from "next/image";
import Link from "next/link";
import { Button } from "@mui/material";
import SaveIcon from '@mui/icons-material/Save';

export default function Home() {
  return (
    <div className="flex inset-0 fixed flex-col items-center justify-center min-w-96 mx-auto gap-4">
      <div>I am router page</div>
      <Button variant="outlined"><Link href="/users">user info</Link></Button>
      <Button variant="outlined"><Link href="/subscription">Subscription info</Link></Button>
      <Button variant="outlined"><Link href="/userSubscription">user-subscription info</Link></Button>
    </div>
  );
}
