export class OperationsComponent {
  title = 'Telecommunications: Service Provisioning, Network & Incident Operations';
  // Brownfield issue: UI trusts backend decisions and has no field-level masking.
  visibleColumns = ['id', 'status', 'risk_score', 'owner', 'last_updated'];
}
