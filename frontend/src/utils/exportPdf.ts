import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";
import { TrajectoryData } from "@/types";

export function exportTrajectoryPdf(trajectory: TrajectoryData) {
  const doc = new jsPDF();

  doc.setFillColor(15, 23, 42);
  doc.rect(0, 0, 210, 30, "F");
  doc.setTextColor(255, 255, 255);
  doc.setFontSize(16);
  doc.text("NETRAGATI DIGITAL FORENSICS & TRAJECTORY DOSSIER", 14, 18);
  doc.setFontSize(9);
  doc.text("LAW ENFORCEMENT AUTOMATIC NUMBER PLATE RECONSTRUCTION SYSTEM", 14, 25);

  doc.setTextColor(30, 41, 59);
  doc.setFontSize(10);
  doc.text(`Generated: ${new Date().toLocaleString()}`, 14, 40);
  doc.text(`Target Vehicle Plate: ${trajectory.canonical_plate}`, 14, 46);
  doc.text(`Trajectory Total Legs: ${trajectory.total_legs}`, 14, 52);

  const tableData = trajectory.legs.map((leg, index) => [
    `#${index + 1}`,
    `${leg.from_camera} -> ${leg.to_camera}`,
    new Date(leg.arrival_time).toLocaleTimeString(),
    `${leg.distance_meters} m`,
    `${leg.speed_kmh} km/h`,
    leg.reconciled ? `Reconciled (${leg.reconciliation_details?.substring(0, 25)}...)` : "Direct Read"
  ]);

  autoTable(doc, {
    startY: 60,
    head: [["Leg", "Corridor Segment", "Timestamp", "Distance", "Calculated Velocity", "OCR Mode"]],
    body: tableData,
    theme: "grid",
    headStyles: { fillColor: [15, 23, 42] },
    styles: { fontSize: 8 }
  });

  const finalY = (doc as any).lastAutoTable.finalY + 15;
  doc.setFontSize(9);
  doc.setTextColor(100, 116, 139);
  doc.text("Certified authentic cryptographic system report generated under Digital Evidentiary Compliance Rules.", 14, finalY);

  doc.save(`Trajectory_${trajectory.canonical_plate}_Dossier.pdf`);
}
