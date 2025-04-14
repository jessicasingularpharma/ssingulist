// frontend/src/components/ui/dialog.tsx

import { Dialog as HeadlessDialog, Transition } from "@headlessui/react";
import { Fragment, ReactNode } from "react";

interface DialogProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: ReactNode;
}

export const CustomDialog = ({ isOpen, onClose, title, children }: DialogProps) => {
  return (
    <Transition appear show={isOpen} as={Fragment}>
      <HeadlessDialog as="div" className="relative z-50" onClose={onClose}>
        <Transition.Child
          as={Fragment}
          enter="ease-out duration-200"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="ease-in duration-100"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <div className="fixed inset-0 bg-black bg-opacity-30" />
        </Transition.Child>

        <div className="fixed inset-0 flex items-center justify-center p-4">
          <Transition.Child
            as={Fragment}
            enter="ease-out duration-200"
            enterFrom="opacity-0 scale-95"
            enterTo="opacity-100 scale-100"
            leave="ease-in duration-100"
            leaveFrom="opacity-100 scale-100"
            leaveTo="opacity-0 scale-95"
          >
            <HeadlessDialog.Panel className="w-full max-w-2xl transform overflow-hidden rounded-lg bg-white p-6 text-left align-middle shadow-xl transition-all">
              {title && (
                <HeadlessDialog.Title className="text-lg font-semibold text-gray-800 mb-4">
                  {title}
                </HeadlessDialog.Title>
              )}
              {children}
              <div className="mt-6 text-right">
                <button
                  onClick={onClose}
                  className="px-4 py-2 text-sm rounded bg-blue-600 text-white hover:bg-blue-700 transition"
                >
                  Fechar
                </button>
              </div>
            </HeadlessDialog.Panel>
          </Transition.Child>
        </div>
      </HeadlessDialog>
    </Transition>
  );
};
