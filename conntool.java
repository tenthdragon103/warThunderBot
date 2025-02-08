import java.util.ArrayList;
import java.util.Scanner;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.FileReader;
import java.lang.StringBuilder;

class conntool {

    private static final String BANPATH = "banned_users.txt";
    private static final String WARNPATH = "warns.txt";
    private static final String COMPLAINTPATH = "complaints.txt";

    public static void main(String[] args) {
		System.out.println("Initializing process. Filepaths:");
		System.out.println(BANPATH + "\n" + WARNPATH + "\n" + COMPLAINTPATH + "\n*******************\n");	
		conntool ct = new conntool();
		Scanner in = new Scanner(System.in);
		String cmd;

		while (true) {
			cmd = in.nextLine().trim();
			String[] cmdargs = cmd.split("\\s+");
			
			if (cmd.equalsIgnoreCase("exit")) {
				break;
			}

			switch(cmdargs[0]) {
				case "ban":
					if (cmdargs.length > 1) {
						System.out.println("Banned " + cmdargs[1]);
					} else {
						System.out.println("Incomplete ban command.");
					}
					break;
				case "warn":
					if (cmdargs.length > 1) {
						System.out.println("Warned " + cmdargs[1]);
					} else {
						System.out.println("Incomplete warn command.");
					}
					break;
				case "kick":
					if (cmdargs.length > 1) {
						System.out.println("Kicked " + cmdargs[1]);
					} else {
						System.out.println("Incomplete kick command.");
					}
					break;
				case "detail":
					if (cmdargs.length > 1) {
						ct.overviewPlayer(cmdargs[1]);
					} else {
						System.out.println("Incomplete detail command.");
					}
					break;
				default:
					System.out.println("Command unrecognized.");
			}

		}
    }

    public void overviewPlayer(String player) {
		System.out.println("**** " + player + " ****");
		System.out.println((checkBan(player)) ? "Banned: true" : "Banned: false" );
		System.out.println("Total warnings: " + checkWarns(player));
		ArrayList<String> complaintlist = checkComplaints(player);
		System.out.println("Complaints:");
		for (int i = 0; i < complaintlist.size(); i++) System.out.println(complaintlist.get(i));
		System.out.println("*****" + "*".repeat(player.length()) + "*****");
    }

    public boolean checkBan(String player) {
		String line;
		try (BufferedReader reader = new BufferedReader(new FileReader(BANPATH))) {
			while ((line = reader.readLine()) != null) {
                if (line.contains(player)) {
                    return true;
                }
			}
		} catch (IOException e) {
            System.out.println("Error reading file: " + e.getMessage());
        }
		return false;
    }

    public int checkWarns(String player) {
		String line;
		try (BufferedReader reader = new BufferedReader(new FileReader(WARNPATH))) {
			while ((line = reader.readLine()) != null) {
                String[] warnargs = line.split("\\s+");
				if (warnargs.length == 2 && warnargs[0].equals(player)) {
					return Integer.parseInt(warnargs[1]);
				}
			}
		} catch (IOException e) {
            System.out.println("Error reading file: " + e.getMessage());
        }
		return 0;
    }

    public ArrayList<String> checkComplaints(String player) {
		ArrayList<String> list = new ArrayList<String>();
		//syntax: "<target> <issuer> <reason>

		try (BufferedReader reader = new BufferedReader(new FileReader(COMPLAINTPATH))) {
			String line;
			while ((line = reader.readLine()) != null) {
                String[] comargs = line.split("\\s+");
				if (comargs.length > 2 && comargs[0].equals(player)) {
					StringBuilder sb = new StringBuilder(comargs[1] + ":");
					for (int i = 2; i < comargs.length; i++) sb.append(" " + comargs[i]);
					list.add(sb.toString());
				}
			}
		} catch (IOException e) {
            System.out.println("Error reading file: " + e.getMessage());
        }

		return list;
    }
}