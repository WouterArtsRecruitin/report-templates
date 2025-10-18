import React, { useState } from 'react';
import { X, CreditCard, Download, CheckCircle, Lock } from 'lucide-react';
import { Button } from './ui/button';
import { ReportData } from '../types/report';

interface CheckoutModalProps {
  isOpen: boolean;
  onClose: () => void;
  reportData: ReportData;
  onPaymentSuccess: (reportData: ReportData) => void;
}

export function CheckoutModal({ isOpen, onClose, reportData, onPaymentSuccess }: CheckoutModalProps) {
  const [step, setStep] = useState<'details' | 'payment' | 'processing' | 'success'>('details');
  const [formData, setFormData] = useState({
    email: '',
    name: '',
    company: '',
    cardNumber: '',
    expiryDate: '',
    cvv: ''
  });

  if (!isOpen) return null;

  const handlePayment = () => {
    setStep('processing');
    // Simulate payment processing
    setTimeout(() => {
      setStep('success');
      // Trigger report download after payment
      setTimeout(() => {
        onPaymentSuccess(reportData);
        onClose();
      }, 2000);
    }, 3000);
  };

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-md w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-slate-200">
          <h2 className="text-xl text-slate-900">Download Market Intelligence</h2>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-600">
            <X className="w-5 h-5" />
          </button>
        </div>

        {step === 'details' && (
          <div className="p-6">
            {/* Order Summary */}
            <div className="bg-blue-50 border-l-4 border-blue-600 p-4 rounded-r-lg mb-6">
              <h3 className="text-blue-900 mb-2">{reportData.config.title}</h3>
              <div className="text-sm text-slate-600 space-y-1">
                <div>{reportData.config.subtitle}</div>
                <div>• {reportData.config.totalPages} pagina's volledige analyse</div>
                <div>• PDF + Printable formaat</div>
                <div>• 30 dagen gratis updates</div>
              </div>
              <div className="mt-3 pt-3 border-t border-blue-200">
                <div className="flex justify-between items-center">
                  <span className="text-blue-900">Totaal</span>
                  <span className="text-2xl text-blue-900">{reportData.config.currency}{reportData.config.price}</span>
                </div>
              </div>
            </div>

            {/* Contact Form */}
            <div className="space-y-4 mb-6">
              <div>
                <label className="block text-sm text-slate-700 mb-1">Email adres *</label>
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => handleInputChange('email', e.target.value)}
                  className="w-full p-3 border border-slate-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="jouw@email.com"
                  required
                />
              </div>
              <div>
                <label className="block text-sm text-slate-700 mb-1">Volledige naam *</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => handleInputChange('name', e.target.value)}
                  className="w-full p-3 border border-slate-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="Voor- en achternaam"
                  required
                />
              </div>
              <div>
                <label className="block text-sm text-slate-700 mb-1">Bedrijfsnaam (optioneel)</label>
                <input
                  type="text"
                  value={formData.company}
                  onChange={(e) => handleInputChange('company', e.target.value)}
                  className="w-full p-3 border border-slate-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="Jouw bedrijf"
                />
              </div>
            </div>

            <Button 
              onClick={() => setStep('payment')}
              className="w-full bg-blue-700 hover:bg-blue-800 h-12"
              disabled={!formData.email || !formData.name}
            >
              Ga naar betaling
            </Button>
          </div>
        )}

        {step === 'payment' && (
          <div className="p-6">
            <div className="mb-6">
              <h3 className="text-lg text-slate-900 mb-2">Betaalgegevens</h3>
              <div className="text-sm text-slate-600">
                Beveiligde betaling via Stripe • SSL versleuteling
              </div>
            </div>

            <div className="space-y-4 mb-6">
              <div>
                <label className="block text-sm text-slate-700 mb-1">Kaartnummer *</label>
                <div className="relative">
                  <input
                    type="text"
                    value={formData.cardNumber}
                    onChange={(e) => handleInputChange('cardNumber', e.target.value)}
                    className="w-full p-3 pl-10 border border-slate-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    placeholder="1234 5678 9012 3456"
                    required
                  />
                  <CreditCard className="w-5 h-5 text-slate-400 absolute left-3 top-3.5" />
                </div>
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm text-slate-700 mb-1">Vervaldatum *</label>
                  <input
                    type="text"
                    value={formData.expiryDate}
                    onChange={(e) => handleInputChange('expiryDate', e.target.value)}
                    className="w-full p-3 border border-slate-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    placeholder="MM/YY"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm text-slate-700 mb-1">CVV *</label>
                  <input
                    type="text"
                    value={formData.cvv}
                    onChange={(e) => handleInputChange('cvv', e.target.value)}
                    className="w-full p-3 border border-slate-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    placeholder="123"
                    required
                  />
                </div>
              </div>
            </div>

            <div className="flex items-center gap-2 mb-6 text-xs text-slate-600">
              <Lock className="w-4 h-4" />
              <span>Je betaalgegevens zijn beveiligd met 256-bit SSL encryptie</span>
            </div>

            <div className="space-y-3">
              <Button 
                onClick={handlePayment}
                className="w-full bg-blue-700 hover:bg-blue-800 h-12"
                disabled={!formData.cardNumber || !formData.expiryDate || !formData.cvv}
              >
                Betaal {reportData.config.currency}{reportData.config.price}
              </Button>
              <button
                onClick={() => setStep('details')}
                className="w-full text-slate-600 hover:text-slate-800 text-sm"
              >
                ← Terug naar gegevens
              </button>
            </div>
          </div>
        )}

        {step === 'processing' && (
          <div className="p-6 text-center py-12">
            <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <div className="w-8 h-8 border-3 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
            </div>
            <h3 className="text-lg text-slate-900 mb-2">Betaling wordt verwerkt...</h3>
            <p className="text-slate-600 text-sm">
              Even geduld terwijl we je betaling beveiligen en je rapport voorbereiden.
            </p>
          </div>
        )}

        {step === 'success' && (
          <div className="p-6 text-center py-12">
            <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <CheckCircle className="w-10 h-10 text-green-600" />
            </div>
            <h3 className="text-lg text-slate-900 mb-2">Betaling succesvol!</h3>
            <p className="text-slate-600 text-sm mb-6">
              Je rapport wordt nu gegenereerd en automatisch gedownload.
              Je ontvangt ook een email met de downloadlink.
            </p>
            <div className="flex items-center gap-2 justify-center text-sm text-green-700 bg-green-50 p-3 rounded">
              <Download className="w-4 h-4" />
              <span>Download start automatisch...</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}